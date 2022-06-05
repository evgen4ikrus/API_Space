import requests
import os
from urllib.parse import unquote, urlparse
from dotenv import load_dotenv
import datetime
import telegram


def image_download(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
        

def get_image_extension(url):
    image_url = urlparse(url).path
    image_url = unquote(image_url, encoding='utf-8', errors='replace')
    name_image = os.path.split(image_url)[1]
    image_expansion = os.path.splitext(name_image)[1]
    return image_expansion


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v3/launches'
    payload = {
    'flight_number': '75',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    photos_links = response.json()[0]['links']['flickr_images']
    for image_number, photo_link in enumerate(photos_links):
        image_expansion = get_image_extension(photo_link)
        image_path = f'images/spacex_{image_number}{image_expansion}'
        image_download(photo_link, image_path)
        
        
def fetch_nasa_epic_photo(token):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': token,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    epic_photos = response.json()
    for link_number, photo in enumerate(epic_photos[:7]):
        url = 'https://api.nasa.gov/EPIC/archive/natural'
        photo_datetime = datetime.datetime.fromisoformat(photo['date'])
        photo_year = photo_datetime.strftime('%Y')
        photo_month = photo_datetime.strftime('%m')
        photo_day = photo_datetime.strftime('%d')
        file_name = photo['image']
        response = requests.get(f'{url}/{photo_year}/{photo_month}/{photo_day}/png/{file_name}.png', params=payload)
        image_url = response.url
        image_expansion = get_image_extension(image_url)
        path = f'images/epic_photo_{link_number}{image_expansion}'
        image_download(image_url, path)


def fetch_nasa_photo_day(token):
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': token,
        'count':10,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    photo_day_links = response.json()
    for link_number, photo_day_link in enumerate(photo_day_links):
        if 'hdurl' in photo_day_link:
            image_url = photo_day_link['hdurl']
            image_expansion = get_image_extension(image_url)
            path = f'images/nasa_apod_{link_number}{image_expansion}'
            image_download(image_url, path)


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_TOKEN"]
    if not os.path.exists('images/'):
        os.makedirs('images/')
    # fetch_spacex_last_launch()
    # fetch_nasa_photo_day(nasa_token)
    # fetch_nasa_epic_photo(nasa_token)
    
    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    bot = telegram.Bot(token=telegram_token)
    chat_id = '@sergeevichevgeniy'
    # bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
    bot.send_document(chat_id=chat_id, document=open('images/spacex_0.jpg', 'rb'))
    
if __name__=='__main__':
    main()




