import os
import random
import time

import telegram
from dotenv import load_dotenv

from fetch_nasa_day_photo import fetch_nasa_day_photo
from fetch_nasa_epic_photos import fetch_nasa_epic_photos
from fetch_spacex_images import fetch_spacex_last_launch
from nasa_spacex_functions import get_file_names


def publish_image_to_telegram(image, telegram_token, telegram_chat_id):
    bot = telegram.Bot(token=telegram_token)
    bot.send_document(chat_id=telegram_chat_id,
                      document=open(f'images/{image}', 'rb'))


def endlessly_sends_pictures_for_publication(telegram_token,
                                             publication_delay,
                                             telegram_chat_id,
                                             nasa_token,
                                             images_count,
                                             photo_creation_epic_date,
                                             flight_number):
    while True:
        os.makedirs('images/', exist_ok=True)
        images = get_file_names('images/')
        if not images:
            fetch_spacex_last_launch(flight_number)
            fetch_nasa_day_photo(nasa_token, images_count)
            fetch_nasa_epic_photos(nasa_token, photo_creation_epic_date)
            images = get_file_names('images/')
        image = random.choice(images)
        image_size = os.stat(f'images/{image}').st_size
        if image_size < 20000000:
            publish_image_to_telegram(image, telegram_token, telegram_chat_id)
            time.sleep(int(publication_delay))
        os.remove(f'images/{image}')


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    publication_delay = os.getenv('PUBLICATION_DELAY', default=14400)
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    nasa_token = os.getenv('NASA_TOKEN')
    images_count = os.getenv('IMAGES_NASA_COUNT', default=10)
    photo_creation_epic_date = os.getenv('PHOTO_CREATING_EPIC_DATE',
                                         default='2022-06-05')
    flight_number = os.getenv('SPACEX_FLIGHT_NUMBER', default=25)
    endlessly_sends_pictures_for_publication(telegram_token,
                                             publication_delay,
                                             telegram_chat_id,
                                             nasa_token,
                                             images_count,
                                             photo_creation_epic_date,
                                             flight_number)
