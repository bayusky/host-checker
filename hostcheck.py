import os
import csv
import sys
try:
    import requests
except Exception:
    print("No module 'requests' found. Install: pip3 install requests")
    sys.exit(1) 

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
            

#open host csv file
try:
    csv_file = open('hostlist.csv')
except OSError:
    print("File not found, check availability or permission of hostlist.csv")

# set message
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
            stream = os.popen('ping -c 4 {}'.format(ip_addr)) 
            
            #check feedback from host
            output = stream.read()
            if '0 received' in output: 
                message += f"\n{hostname} status: ---OFFLINE--"
            else: 
                message += f"\n{hostname} status: Online"
            line_count += 1
          

#hook to bot API
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#send messages
(requests.get(url).json())

