import csv
import requests

#insert bot API token and your chat-id
TOKEN = "insert your token here"
chat_id = "insert your chat_id here"

message = "Website connection status : "

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
            
            try:
                #send GET to http / https
                response = requests.get(url, verify=False)
            except requests.exceptions.Timeout as e: #if error timeout
                message += f"\n{hostname} timeout"
            
            else:
                #get response status code
                status = response.status_code
                #if connection success (response code 200)
                if status == 200 : 
                    message += f"\n{hostname} webservice online"
                else:
                    message += f"\n{hostname} response status {status}"
            
            line_count += 1
          


url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
(requests.get(url).json()) # this sends the message

