import re
from pathlib import Path, PurePath
from urllib.parse import urlsplit

import requests


def download(page_url: str, output_dir: str) -> Path:
    page_url.rstrip('.')
    print(page_url)
    file_name = create_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    response = requests.get(page_url)
    file_path.write_bytes(response.content)
    dir_name = create_dir_name(page_url)
    Path(output_dir, dir_name).mkdir(exist_ok=True)
    return file_path


def create_file_name(page_url: str) -> str:
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '.html']
    return ''.join(jj)


def create_dir_name(page_url: str) -> str:
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '_files']
    return ''.join(jj)
