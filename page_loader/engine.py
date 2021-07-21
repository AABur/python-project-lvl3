# -*- coding:utf-8 -*-
"""Download the content of the given HTML file and return the content.

Returns:
    str: local HTML page
"""

import logging
import sys
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

logger = logging.getLogger('page-loader')

TAGS = ('link', 'script', 'img')


def download(page_url: str, target_dir: str = '') -> str:
    resources_dir_name = compose_local_name(page_url, is_dir=True)
    page_file_path = Path(target_dir, compose_local_name(page_url))
    logger.debug(f'Start downloading {page_url} to {page_file_path}')
    html_page = fetch_html_page(page_url)
    local_html, resources = prepare_soup(html_page, page_url, resources_dir_name)  # noqa: E501
    fetch_resources(resources, Path(target_dir, resources_dir_name))
    Path(page_file_path).write_text(local_html)
    logger.debug(f'Finish downloading {page_url} to {page_file_path}')
    return str(page_file_path)


def fetch_html_page(page_url: str) -> str:
    try:
        response = requests.get(page_url)
    except Exception:
        logger.error('Failed access', exc_info=True)
        sys.exit(0)
    return response.text


def prepare_soup(html_page, page_url: str, resources_dir_name: str) -> Any:  # noqa: WPS210, E501
    soup = BeautifulSoup(html_page, 'lxml')
    resources = {}
    page_url = page_url if page_url.endswith('/') else f'{page_url}/'
    for source_tag in soup.find_all(TAGS):
        attribute_name = 'src' if source_tag.name in {
            'script', 'img',
        } else 'href'
        full_resource_url = urljoin(page_url, source_tag.get(attribute_name))
        if urlparse(full_resource_url).netloc == urlparse(page_url).netloc:
            local_file_name = compose_local_name(full_resource_url)
            resources[full_resource_url] = local_file_name
            source_tag[attribute_name] = Path(
                resources_dir_name, local_file_name,
            )
    local_html_page = soup.prettify(formatter='html5')
    return local_html_page, resources


def fetch_resources(resources, resources_local_dir: Path) -> None:
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
            except ConnectionError:
                logger.error('Failed access resource', exc_info=True)
            except IOError:
                logger.error('Failed write resource file', exc_info=True)
            bar.next()  # noqa:B305
    logger.debug('Finish downloading resources')


def download_file(url, local, local_dir):
    response = requests.get(url)
    with open(Path(local_dir, local), 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)


def compose_local_name(resource_url: str, is_dir: bool = False) -> str:
    """Compose a path name for a resource.

    Args:
        resource_url (str): resource url
        is_dir (bool): resource type

    Returns:
        str: resource local file name
    """
    url_parse = urlparse(resource_url)
    ext = Path(url_parse.path).suffix
    full_path = Path(url_parse.netloc + url_parse.path)
    name = re.sub(
        r'\W+',
        '-',
        str(full_path.with_suffix('')),
    )
    if is_dir:
        return '{0}_files'.format(name)
    return '{0}{1}'.format(name, (ext or '.html'))
