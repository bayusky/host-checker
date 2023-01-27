# host-check
Simple python script to check connection to network devices and websites and report it via Telegram Bot.
```host-check``` use csv and request modules from python.
CSV Modules load file contains host list and website list on csv formatted text.
Requests Modules sent messages via Telegram Bot.

*Requirements*
* Python 3
* Request modules, install it using ```pip install requests```
* Fully working telegram bot, as reference you can read it here : https://bayuskylabs.com/integrasi-wazuh-alert-dengan-telegram-bot/ to create fully working telegram bot.

*Usage*
* Download all files
* Insert your API Key and Chat ID to ```hostcheck.py``` and ```webcheck.py```
* ```hostcheck.py``` use ```hostlist.csv``` as the source, so insert your network device's name and IP Address to ```hostlist.csv```
* ```webcheck.py``` use ```weblist.csv``` as the source, so insert your website Name and URL ```to weblist.csv```
* you can remove ```verify=False``` on ```webcheck.py``` on line 27 if your SSL Certificate are not self-signed.
* double check your ```/path/to/csv/files.csv``` on both python files.
* execute using ```python3 /path/to/code.py``` (recommended) or ```python /path/to/code.py``` (for those who has configured python binary path)

*Warning*
* Only use this script on private machine with private IP, for security reasons.

If you find my code useful, I'll gladly accept a [cup of coffee](https://ko-fi.com/bayusky)

