import os
import random
import time

import telegram
from dotenv import load_dotenv

from fetch_nasa_day_photo import fetch_nasa_day_photo
from fetch_nasa_epic_photos import fetch_nasa_epic_photos
from fetch_spacex_images import fetch_spacex_last_launch
from functions import get_file_names, folder_creates

load_dotenv()


telegram_token = os.environ['TELEGRAM_TOKEN'] 
publication_delay = os.getenv('PUBLICATION_DELAY', default=14400)
telegram_chet_id = os.getenv('TELEGRAM_CHAT_ID')


def publish_image_to_telegram(image):
    bot = telegram.Bot(token=telegram_token)
    bot.send_document(chat_id=telegram_chet_id, document=open(f'images/{image}', 'rb'))


def endlessly_sends_pictures_for_publication():
    while 1>0:
        folder_creates()
        images = get_file_names('images/')  
        if not images:
            fetch_spacex_last_launch()
            fetch_nasa_day_photo()
            fetch_nasa_epic_photos()
            images = get_file_names('images/')
        image = random.choice(images)  
        image_size = os.stat(f'images/{image}').st_size
        if image_size < 20000000:
            publish_image_to_telegram(image)
            time.sleep(int(publication_delay))
        os.remove(f'images/{image}')


if __name__=='__main__':
    endlessly_sends_pictures_for_publication()