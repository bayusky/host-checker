import csv
import sys
from cryptography import x509
from datetime import datetime

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

#read botinfo.csv to get API token and your chat-id
try:
    bot_csv = open('botinfo.csv')
except OSError:
    print("File not found, check availability of botinfo.csv")

with bot_csv:
     botinfo = csv.reader(bot_csv, delimiter=';')
     line_count = 0
     for row in botinfo:
        if line_count == 0:
            print("botinfo.csv OK")
            line_count += 1
        else:
            TOKEN = f"{row[0]}"
            chat_id = f"{row[1]}"

#open web csv file
try:
    csv_file = open('weblist.csv')
except OSError:
    print("File not found, check availability or permission of hostlist.csv")

message = "Website and SSL status : "

#open csv file
with open('weblist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #skip header (column name) on first line               
        if line_count == 0 : 
            message +=f"\n-------------------------------"
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
          


url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
(requests.get(url).json()) # this sends the message

