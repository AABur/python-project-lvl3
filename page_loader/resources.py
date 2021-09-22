# -*- coding:utf-8 -*-

import logging
from pathlib import Path
from urllib.parse import urlparse

import requests
from progress.bar import IncrementalBar
from requests.exceptions import RequestException

from page_loader.exceptions import PLIOError, PLNetworkError

logger = logging.getLogger(__name__)

TAGS = ('link', 'script', 'img')


def fetch_resources(resources: dict, resources_local_dir: Path) -> None:
    logger.debug('Start downloading resources')
    Path(resources_local_dir).mkdir()
    with IncrementalBar(
        'Downloading',
        max=len(resources),
        suffix='%(percent).1f%% [%(elapsed)ds]',  # noqa:WPS323
    ) as bar:
        for res_url, res_local in resources.items():
            try:
                download_file(res_url, res_local, resources_local_dir)
            except RequestException:
                logger.error('Failed access resource', exc_info=True)
                raise PLNetworkError
            except IOError:
                logger.error('Failed write resource file', exc_info=True)
                raise PLIOError
            bar.next()  # noqa:B305
    logger.debug('Finish downloading resources')


def is_local_resource(page_url, full_resource_url):
    return urlparse(full_resource_url).netloc == urlparse(page_url).netloc


def download_file(url: str, local: str, local_dir: Path):
    """Download a file from a URL.

    Args:
        url (str): file url
        local (str): file local name
        local_dir (Path): target directory
    """
    response = requests.get(url, stream=True)
    with open(Path(local_dir, local), 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
