import re
from pathlib import Path, PurePath
from urllib.parse import urlsplit

import requests


def download(page_url, output_dir):
    response = requests.get(page_url)
    file_name = create_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    file_path.write_text(response.text)
    return file_path


def create_file_name(page_url):
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '.html']
    return ''.join(jj)
