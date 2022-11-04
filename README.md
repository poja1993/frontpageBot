# frontpageBot
Retrive selected newspapers' front pages from https://www.frontpages.com/ and send them via Telegram bot to a specific chat

## Installation
* Install the following dependencies (i.e. via pip install):
  * requests
  * telegram
  * bs4  
* Modify the config.json with the following:
  * Bot Token 
  * Chat id
  * Newspaper sub-url (it's possible to add/remove newspapers)
* Execute the script daily with a cronjob or triggered by Home Assistant (in progress) and enjoy the reading together with a coffee
