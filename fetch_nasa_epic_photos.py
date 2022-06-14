import datetime
import os

import requests
from dotenv import load_dotenv

from nasa_spacex_functions import get_image_extension, image_download


def fetch_nasa_epic_photos(nasa_token, photo_creation_epic_date):
    os.makedirs('images/', exist_ok=True)
    photo_info_url = f'https://api.nasa.gov/EPIC/api/natural/date/{photo_creation_epic_date}'
    photo_url = 'https://api.nasa.gov/EPIC/archive/natural'
    payload = {
        'api_key': nasa_token,
    }
    response = requests.get(photo_info_url, params=payload)
    response.raise_for_status()
    epic_photos = response.json()
    for link_number, photo in enumerate(epic_photos):
        photo_datetime = datetime.datetime.fromisoformat(photo['date'])
        photo_date = photo_datetime.strftime('%Y/%m/%d')
        file_name = photo['image']
        response = requests.get(f'{photo_url}/{photo_date}/png/{file_name}.png',
                                params=payload)
        image_url = response.url
        image_extension = get_image_extension(image_url)
        path = f'images/epic_photo_{link_number}{image_extension}'
        image_download(image_url, path)


if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    photo_creation_epic_date = os.getenv('PHOTO_CREATING_EPIC_DATE',
                                         default='2022-06-05')
    fetch_nasa_epic_photos(nasa_token, photo_creation_epic_date)
