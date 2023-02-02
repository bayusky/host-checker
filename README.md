# host-checker
Simple python script to check connection to network devices, websites, and ssl expiration date. Then send the report it via Telegram or Slack Bot.
```host-checker``` use .env to put configuration parameter and csv files to simplified adding data to execute.

*Files used, make sure you rename it first*
* ```.env``` contains Telegram and Slack parameter. Rename ```.env.template``` to ```.env```
* ```hostlist.csv``` contains network device's name and IP Address. rename ```hostlist.csv.template``` to ```hostlist.csv```
* ```weblist.csv``` contains domain or subdomain name *only* (without http:// or https://). Rename ```weblist.csv.template``` to ```weblist.csv```

*Requirements*
* Python 3
* Request modules, install it using ```pip3 install requests```
* OpenSSL modules, install it using ```pip3 install pyOpenSSL```
* Cryptography modules, install it using ```pip3 install cryptography```
* Dotenv modules, install it using ```pip3 install python-dotenv```
* Fully working telegram bot, as reference you can read it here : https://bayuskylabs.com/integrasi-wazuh-alert-dengan-telegram-bot/ to create fully working telegram bot.
* Fully working slack channel and webhook.

*Usage*
* Download all files
* Insert your telegram/slack parameters to ```.env```
* ```hostcheck.py``` use ```hostlist.csv``` as the source, so insert your network device's name and IP Address to ```hostlist.csv```
* ```webcheck.py``` and ```sslcheck``` use ```weblist.csv``` as the source, so insert your website Name and domain/subdomain ```to weblist.csv```
* ```host-web-checker.py``` is a script to check network devices and webservice status.
* ```sslcheck``` is a script to check your SSL expired date.
* you can uncomment ```verify=False``` on ```webcheck.py```, ```sslcheck.py```, or ```host-web-checker.py``` if your SSL Certificate are self-signed.
* double check your ```*.csv``` and ```.env``` to avoid error.
* execute using ```python3 /path/to/code.py``` (recommended) or ```python /path/to/code.py``` (for those who has configured python as an alias for python3)
* You can make a cronjob for periodical check.

*Warning*
* Only use this script on private machine with private IP, for security reasons.

If you find my code useful, I'll gladly accept a [cup of coffee](https://ko-fi.com/bayusky)

