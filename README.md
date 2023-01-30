# host-check
Simple python script to check connection to network devices and websites (+ssl expired date) and report it via Telegram Bot.
```host-check``` use csv, requests, and OpenSSL (pyOpenSSL) modules from python.
CSV files usage :
* ```botinfo.csv``` contains API Key dan chat-ID for telegram bot
* ```hostlist.csv``` contains network device's name and IP Address
* ```weblist.csv``` contains domain or subdomain name *only* (without http:// or https://)
Requests Modules sent messages via Telegram Bot.

*Requirements*
* Python 3
* Request modules, install it using ```pip install requests```
* Fully working telegram bot, as reference you can read it here : https://bayuskylabs.com/integrasi-wazuh-alert-dengan-telegram-bot/ to create fully working telegram bot.

*Usage*
* Download all files
* Insert your API Key and Chat ID to ```botinfo.csv```
* ```hostcheck.py``` use ```hostlist.csv``` as the source, so insert your network device's name and IP Address to ```hostlist.csv```
* ```webcheck.py```, ```sslcheck``` use ```weblist.csv``` as the source, so insert your website Name and domain/subdomain ```to weblist.csv```
* ```host-web-ssl-checker.py``` is all-in-one script to check network devices, webservice status, and SSL espired date.
* you can uncomment ```verify=False``` on ```webcheck.py```, ```sslcheck.py```, or ```host-web-ssl-checker.py``` if your SSL Certificate are self-signed.
* double check your ```/path/to/csv/files.csv``` or just leave csv files on the same directory to avoid error.
* execute using ```python3 /path/to/code.py``` (recommended) or ```python /path/to/code.py``` (for those who has configured python as an alias for python3)

*Warning*
* Only use this script on private machine with private IP, for security reasons.

If you find my code useful, I'll gladly accept a [cup of coffee](https://ko-fi.com/bayusky)

