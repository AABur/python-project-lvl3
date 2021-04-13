import re
from pathlib import Path, PurePath
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup


def download(page_url, output_dir):
    file_name = create_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'lxml')
    images = soup.find_all('img')
    for image in images:
        print(image.get('src'))
    file_path.write_text(response.text)
    return file_path


def create_file_name(page_url):
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '.html']
    return ''.join(jj)
