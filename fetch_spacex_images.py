import os

import requests

from nasa_spacex_functions import folder_creates, get_image_extension, image_download


def fetch_spacex_last_launch():
    folder_creates()
    url = 'https://api.spacexdata.com/v3/launches'
    flight_number = os.getenv('SPACEX_FLIGHT_NUMBER', default=25)
    payload = {
    'flight_number': flight_number,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    try:
        photos_links = response.json()[0]['links']['flickr_images']
    except IndexError:
        exit(f"Запуска с номером: {flight_number} не было")
    for image_number, photo_link in enumerate(photos_links):
        image_extension = get_image_extension(photo_link)
        image_path = f'images/spacex_{image_number}{image_extension}'
        image_download(photo_link, image_path)


if __name__=='__main__':
    fetch_spacex_last_launch()