import os

import requests
from dotenv import load_dotenv

from functions import folder_creates, get_image_extension, image_download


def fetch_nasa_day_photo():
    load_dotenv()
    nasa_token = os.environ["NASA_TOKEN"]
    images_count = os.getenv('IMAGES_NASA_COUNT', default=10)
    folder_creates()
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': nasa_token,
        'count': images_count,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    day_photo_links = response.json()
    for link_number, day_photo_link in enumerate(day_photo_links):
        if 'hdurl' in day_photo_link:
            image_url = day_photo_link['hdurl']
            image_extension = get_image_extension(image_url)
            path = f'images/nasa_apod_{link_number}{image_extension}'
            image_download(image_url, path)


if __name__=='__main__':
    fetch_nasa_day_photo()