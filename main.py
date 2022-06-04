import requests
import os
from urllib.parse import unquote, urlparse


def image_download(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v3/launches'
    payload = {
    'flight_number':'75',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    photos_links = response.json()[0]['links']['flickr_images']
    for image_number, photo_link in enumerate(photos_links):
        image_expansion = get_image_extension(photo_link)
        image_path = f'images/spacex_{image_number}{image_expansion}'
        image_download(photo_link, image_path)


def get_image_extension(url):
    image_url = urlparse(url).path
    image_url = unquote(image_url, encoding='utf-8', errors='replace')
    name_image = os.path.split(image_url)[1]
    image_expansion = os.path.splitext(name_image)[1]
    return image_expansion


def main():
    if not os.path.exists('images/'):
        os.makedirs('images/')
    fetch_spacex_last_launch()
    
if __name__=='__main__':
    main()




