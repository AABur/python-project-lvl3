import os
import re
import sys
from pathlib import Path, PurePath
from urllib.parse import urlsplit

import requests


def download(page_url, output_dir):
    if not os.access(output_dir, os.W_OK):
        sys.exit('ERROR !!!')
    response = requests.get(page_url)
    file_name = create_file_name(page_url)
    file_path = Path(PurePath(output_dir, file_name))
    file_path.write_text(response.text)
    with open(file_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):  # noqa: WPS432
            fd.write(chunk)
    return file_path


def create_file_name(page_url):
    split = urlsplit(page_url)
    nl = re.sub(r'[\W]', '-', split.netloc)  # noqa: W605
    pa = re.sub(r'[\W]', '-', split.path)  # noqa: W605
    jj = [nl, pa, '.html']
    return ''.join(jj)
