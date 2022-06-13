import datetime
import os

import requests
from dotenv import load_dotenv

from nasa_spacex_functions import get_image_extension, image_download


def fetch_nasa_epic_photos():
    os.makedirs('images/', exist_ok=True)
    load_dotenv()
    nasa_token = os.environ["NASA_TOKEN"]
    photo_creation_epic_date = os.getenv('PHOTO_CREATING_EPIC_DATE', default='2022-06-05')
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{photo_creation_epic_date}'
    payload = {
        'api_key': nasa_token,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    epic_photos = response.json()
    for link_number, photo in enumerate(epic_photos):
        photo_datetime = datetime.datetime.fromisoformat(photo['date'])
        url = 'https://api.nasa.gov/EPIC/archive/natural'
        photo_year = photo_datetime.strftime('%Y')
        photo_month = photo_datetime.strftime('%m')
        photo_day = photo_datetime.strftime('%d')
        file_name = photo['image']
        response = requests.get(f'{url}/{photo_year}/{photo_month}/{photo_day}/png/{file_name}.png', params=payload)
        image_url = response.url
        image_extension = get_image_extension(image_url)
        path = f'images/epic_photo_{link_number}{image_extension}'
        image_download(image_url, path)


if __name__=='__main__':
    fetch_nasa_epic_photos()