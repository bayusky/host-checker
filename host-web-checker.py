import csv
import sys
from datetime import datetime
import os
import json

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


load_dotenv()
try:
    comm_app = os.environ.get('COMM_APP')            
except Exception:
    print("can't read .env, make sure .env configurd properly")
    sys.exit()
            
timestamp = datetime.now()
current_time = timestamp.strftime("%d-%m-%Y, %H:%M")

###############################################################
##                  Network Device Ping Check                ## 
###############################################################

#open host csv file
try:
    csv_file = open('hostlist.csv')
except OSError:
    print("File not found, check availability or permission of hostlist.csv")


with csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #skip header (column name) on first line
        if line_count == 0 : 
            message = ""
            line_count +=1
        else :
            #put data into variable
            hostname = row[0]
            ip_addr = row[1]
             
            #do ping host 
            stream = os.popen('ping -c 4 {}'.format(ip_addr)) 
            
            #check feedback from host
            output = stream.read()
            if '0 received' in output: 
                message += f"\n{hostname} status: ---OFFLINE--"
            else: 
                message += f"\n{hostname} status: Online"
            line_count += 1
          
if comm_app == "slack": #if slack was choosen
    url = os.environ.get('WEBHOOK')
    bot_name = os.environ.get('BOT_NAME')
    channel = os.environ.get('CHANNEL')
    emoji_id = os.environ.get('EMOJI_ID') 
    title = f"Host status {current_time} :"
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
    title = f"Host status {current_time}: "
    title += f"\n-------------------------------"
    #hook to bot API
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={title+message}"
    #send messages
    (requests.get(url).json())
else:
    print(".env not configured properly")


###############################################################
##                    Web Service Checker                    ## 
###############################################################


#open web csv file
try:
    csv_file = open('weblist.csv')
except OSError:
    print("File not found, check availability or permission of weblist.csv")


#open web csv file
with csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        
        #skip header (column name) on first line               
        if line_count == 0 : 
            message_web = ""
            line_count +=1
        else :
            #put csv data into variable
            hostname = row[0]
            url = row[1]
            print(f"https://{url}")
            try:
                #send GET to http / https
                response = requests.get(f"https://{url}") #verify=False)
            except requests.exceptions.Timeout as e: #if error timeout
                message_web += f"\n{hostname} timeout or SSL self-signed, try verify=False on line 113"
            
            else:
                #get response status code
                status = response.status_code

                #if connection success (response code 200)
                if status == 200 : 
                    message_web += f"\n{hostname} webservice online"
                    
                else:
                    message_web += f"\n{hostname} response status {status}"
                
            line_count += 1
          

if comm_app == "slack": #if slack was choosen
    url = os.environ.get('WEBHOOK')
    bot_name = os.environ.get('BOT_NAME')
    channel = os.environ.get('CHANNEL')
    emoji_id = os.environ.get('EMOJI_ID') 
    title = f"Website status {current_time}:"
    slack_data = {
        "username": bot_name,
        "icon_emoji": emoji_id,
        "channel": channel,
        "attachments": [
            {
                "fields": [
                    {
                        "title": title,
                        "value": message_web,
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
    title_web = f"Website status {current_time}: "
    title_web += f"\n-------------------------------"
    #hook to bot API
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={title_web+message_web}"
    #send messages
    (requests.get(url).json())
else:
    print(".env not configured properly")