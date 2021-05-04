import re
from pathlib import Path, PurePath
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup


def download(page_url, output_dir):
    # download html
    file_name = create_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    response = requests.get(page_url)
    file_path.write_bytes(response.content)
    return file_path


def create_file_name(page_url):
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '.html']
    return ''.join(jj)
