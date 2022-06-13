import os
from urllib.parse import unquote, urlparse

import requests


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


def get_file_names(path):
    file_names = []
    for image_name in os.listdir(path):
        file_names.append(image_name)
    return file_names
