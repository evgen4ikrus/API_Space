import os
import random
import time

import telegram
from dotenv import load_dotenv

from fetch_nasa_day_photo import fetch_nasa_day_photo
from fetch_nasa_epic_photos import fetch_nasa_epic_photos
from fetch_spacex_images import fetch_spacex_last_launch
from functions import get_file_names

load_dotenv()


telegram_token = os.environ['TELEGRAM_TOKEN'] 
delay = os.getenv('DELAY', default=10)


def publish_image_to_telegram(image):
    bot = telegram.Bot(token=telegram_token)
    chat_id = '@sergeevichevgeniy'
    bot.send_document(chat_id=chat_id, document=open(f'images/{image}', 'rb'))
    

def endlessly_sends_pictures_for_publication():
    while 1>0:
        images = get_file_names('images/')  
        if not images:
            fetch_spacex_last_launch()
            fetch_nasa_day_photo()
            fetch_nasa_epic_photos()
            images = get_file_names('images/')
        image = random.choice(images)
        publish_image_to_telegram(image)
        os.remove(f'images/{image}')
        time.sleep(int(delay))


endlessly_sends_pictures_for_publication()