import sys
import requests
import telegram
import json
from bs4 import BeautifulSoup as bs

def get_images(data):
    """
    Get from config.json the newspapers' urls, find picture in the webpage and create a list of InputMediaPhoto to send via Telegram Bot
    """
    images = [] # Init list to pass to Telegram Bot
    for newspaper in data["newspapers"]: # Loop for each newspaper defined in json
        url = data["base_url"] + newspaper # "https://www.frontpages.com/" + newspaper Create url string for each newspaper in json
        response = requests.get(url)
        if response.status_code == 200: # Continue if response is succesful
            # Parse the response and look for urls related to images
            soup = bs(response.text, 'html.parser') 
            metas = soup.find_all('meta')
            links = [ meta.attrs['content'] for meta in metas
                     if 'property' in meta.attrs and meta.attrs['property'] == 'og:image' ]
            for link in links:
                if newspaper in link and "jpg" in link: # Get only url that contains jpg in it
                    image = requests.get(link)
                    if image.status_code == 200: # If response is successful, we have our picture. Add it to a list
                        if len(images) == 0: # Put caption only at first item of the list in order to see it in the chat
                            images.append(telegram.InputMediaPhoto(link, caption = "Your today's press release"))
                        else:
                            images.append(telegram.InputMediaPhoto(link))
                        break # No need to look for other urls, one is enough
                    else:
                        print("Error in retrieving picture of " + newspaper)
        else:
            print("Error in finding website for " + newspaper)
    return images

def main():
    """
    Open config file, connect to bot, get relevant data and send pictures via Telegram Bot
    """
    try:
        with open("config.json") as f:
            data = json.load(f)
            try:
                bot = telegram.Bot(token=data["telegram"]["bot_token"])
                if bot.get_me(): # Check connection with bot
                    print("Bot Connected")
            except:
                sys.exit("Cannot connect to bot, check token")
    except IOError:
        sys.exit("Cannot open config.json")
        
    images = get_images(data) # Get pictures from defined url(s)
    if images:
        bot.send_media_group(chat_id=data["telegram"]["chat_id"], media=images)
    else:
        print("else")
        bot.send_message(chat_id=data["telegram"]["chat_id"], text="Sorry, I cannot retrive newspapers pictures!")

if __name__ == '__main__':
    main()
