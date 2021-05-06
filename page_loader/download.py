import os
import re
from pathlib import Path, PurePath
from urllib.parse import urlparse, urlsplit

import requests


def download(page_url: str, output_dir: str) -> Path:
    file_name = generate_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    response = requests.get(page_url)
    file_path.write_bytes(response.content)
    dir_name = generate_dir_name(page_url)
    Path(output_dir, dir_name).mkdir(exist_ok=True)
    return file_path


def generate_file_name(url):
    result_url_parse = urlparse(url)
    path, ext = os.path.splitext(result_url_parse.path)
    filename = replace_chars(result_url_parse.netloc + path)
    ext = ext or '.html'
    return filename + ext


def replace_chars(s):
    return re.sub(re.compile(r'[^0-9a-zA-Z]+'), '-', s)


def generate_dir_name(url_name: str) -> str:
    split = urlsplit(url_name)
    nl = re.sub(r'[\W]', '-', split.netloc)
    pa = re.sub(r'[\W]', '-', split.path)
    jj = [nl, pa, '_files']
    return ''.join(jj)
