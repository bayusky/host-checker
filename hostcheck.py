import os
import csv
import sys
import json
import time
import platform
try:
    from dotenv import load_dotenv
except Exception:
    print("No module 'dotenv' found. Install: pip3 install dotenv")
    sys.exit(1)

try:
    import requests
except Exception:
    print("No module 'requests' found. Install: pip3 install requests")
    sys.exit(1) 

#read environment configuration from .env file
load_dotenv()
try:
    comm_app = os.environ.get('COMM_APP')            
except Exception:
    print("can't read .env, make sure .env configurd properly")
    sys.exit()
    
#open host csv file
try:
    csv_file = open('hostlist.csv')
except OSError:
    print("File not found, check availability or permission of hostlist.csv")

start_time = time.time()
#check platform OS
platform_os = platform.uname()
#print (platform_os)

#set message
message = "Host status : "

#open csv file
with csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
               
        #skip header (column name) on first line
        if line_count == 0 : 
            message +=f"\n-------------------------------"
            line_count +=1
        else :
            #put data into variable
            hostname = row[0]
            ip_addr = row[1]
             
            #do ping host 
            stream = os.popen('ping -n 4 {}'.format(ip_addr)) 
            
            #check feedback from host
            output = stream.read()
            if 'Windows' in platform_os: #if ping run on Windows
                #print(output)
                if 'Received = 0' in output: 
                    message += f"\n{hostname} status: ---OFFLINE--"
                else: 
                    message += f"\n{hostname} status: Online"
            else:
                if '0 Received' in output: 
                    message += f"\n{hostname} status: ---OFFLINE--"
                else: 
                    message += f"\n{hostname} status: Online"
            line_count += 1
          

#if condition to use slack/telegram
if comm_app == "slack":
    url = os.environ.get('WEBHOOK')
    bot_name = os.environ.get('BOT_NAME')
    channel = os.environ.get('CHANNEL')
    emoji_id = os.environ.get('EMOJI_ID') 
    title = "New report!"
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
elif comm_app=="telegram":
    TOKEN = os.environ.get('API_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    #hook to bot API
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    #send messages
    (requests.get(url).json())
else:
    print(".env not configured properly")


#print("--- %s seconds ---" % (time.time() - start_time))