import csv
import sys
import json
import os
from datetime import datetime

try: 
    from cryptography import x509
except Exception:
    print("No module 'cryptography' found. Install: pip3 install cryptography")
    sys.exit(1)

try:
    import requests
except Exception:
    print("No module 'requests' found. Install: pip3 install requests")
    sys.exit(1)

try:
    import OpenSSL
except Exception:
    print("No module 'OpenSSL' found. Install: pip3 install pyOpenSSL")
    sys.exit(1)
import ssl

try:
    from dotenv import load_dotenv
except Exception:
    print("No module 'dotenv' found. Install: pip3 install dotenv")
    sys.exit(1)


#read environment configuration from .env
load_dotenv()
try:
    comm_app = os.environ.get('COMM_APP')            
except Exception:
    print("can't read .env, make sure .env configurd properly")
    sys.exit(1)

timestamp = datetime.now()
current_time = timestamp.strftime("%d-%m-%Y, %H:%M")

#open web csv file
try:
    csv_file = open('weblist.csv')
except OSError:
    print("File not found, check availability or permission of hostlist.csv")


#open csv file
with open('weblist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #skip header (column name) on first line               
        if line_count == 0 : 
            message =""
            line_count +=1
        else :
            #put csv data into variable
            hostname = row[0]
            url = row[1]
            #print(f"https://{url}")
            try:
                #send GET to http / https
                response = requests.get(f"https://{url}") #verify=False)
            except requests.exceptions.Timeout as e: #if error timeout
                message += f"\n{hostname} timeout or SSL self-signed, try verify=False on line 60"
            
            else:
                #get response status code
                status = response.status_code
                #if connection success (response code 200)
                if status == 200 : 
                    #get ssl expired date
                    cert = ssl.get_server_certificate((url,443))
                    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
                    bytes = x509.get_notAfter()
                    #print(bytes)
                    timestamp = bytes.decode('utf-8')
                    expiry_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date().isoformat()
                    message += f"\n{hostname} Certificate expired on {expiry_date}\n"
                else:
                    message += f"\n{hostname} response status {status}"
            
            line_count += 1
          

#if condition to choose between telegram or slack
if comm_app == "slack": #if slack was choosen
    url = os.environ.get('WEBHOOK')
    bot_name = os.environ.get('BOT_NAME')
    channel = os.environ.get('CHANNEL')
    emoji_id = os.environ.get('EMOJI_ID') 
    title = f"Webservice status {current_time} :"
    slack_data = {
        "username": bot_name,
        "icon_emoji": emoji_id,
        "channel": channel,
        "attachments": [
            {
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
elif comm_app=="telegram": #if telegram used
    TOKEN = os.environ.get('API_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    #set message title
    title = f"Webservice status {current_time}: "
    title += f"\n-------------------------------"
    #hook to bot API
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={title+message}"
    #send messages
    (requests.get(url).json())
else:
    print(".env not configured properly")


