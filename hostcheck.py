import os
import csv
import requests
#import json

#insert bot API token and your chat-id
TOKEN = "insert your token her"
chat_id = "insert your chat_id here"

message = "Host check result : "

#open csv file
with open('hostlist.csv') as csv_file:
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

