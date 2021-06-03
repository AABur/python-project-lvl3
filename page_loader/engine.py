# -*- coding:utf-8 -*-
"""Download the content of the given HTML file and return the content.

Returns:
    str: local HTML page
"""
import logging
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import IncrementalBar  # type: ignore

logger = logging.getLogger('page-loader')

TAGS = ('link', 'script', 'img')


def download(page_url: str, target_dir: str = '') -> str:
    """Download the given url to the given path .

    Args:
        page_url (str): page url
        target_dir (str): target dir. Defaults to '.'

    Returns:
        str: local HTML file full path
    """
    local_page_name = compose_local_name(page_url)
    assets_dir_name = compose_local_name(page_url, 'dir')
    page_file_path = Path(target_dir, local_page_name)
    assets_local_dir = Path(target_dir, assets_dir_name)
    logger.debug(f'Start downloading {page_url} to {page_file_path}')
    try:
        Path(assets_local_dir).mkdir()
    except Exception:
        logger.error('Failed to mkdir', exc_info=True)
        sys.exit(1)
    # collect remote assets and prepare local html-page
    local_html = fetch_assets(page_url, assets_dir_name, assets_local_dir)
    try:
        Path(page_file_path).write_text(local_html)  # save html-page locally
    except Exception:
        logger.error('Failed to write file', exc_info=True)
        sys.exit(1)
    logger.debug('Finish downloading {page_url} to {page_file_path}')
    return str(page_file_path)


def fetch_assets(page_url: str, assets_dir_name: str, assets_local_dir: Path) -> Any:  # noqa:WPS210,E501
    """Download assets from given HTML page and store it in assets directory.

    Args:
        page_url (str): given HTML page url
        assets_dir_name (str): assets directory
        assets_local_dir (Path): [description]

    Returns:
        Any: [description]
    """
    logger.debug('Start downloading assets')
    soup = BeautifulSoup(requests.get(page_url).text, 'lxml')
    page_url = page_url if page_url.endswith('/') else f'{page_url}/'
    with IncrementalBar(
        'Downloading',
        max=len(soup.find_all(TAGS)),
        suffix='%(percent).1f%% [%(elapsed)ds]',  # noqa:WPS323
    ) as bar:
        for source_tag in soup.find_all(TAGS):
            attribute_name = 'src' if source_tag.name in {
                'script', 'img',
            } else 'href'
            full_asset_url = urljoin(page_url, source_tag.get(attribute_name))
            if urlparse(full_asset_url).netloc == urlparse(page_url).netloc:
                local_file_name = compose_local_name(full_asset_url)
                try:
                    get_asset(assets_local_dir, full_asset_url, local_file_name)
                except ConnectionError:
                    logger.error('Failed access asset', exc_info=True)
                    sys.exit(1)
                except IOError:
                    logger.error('Failed write asset file', exc_info=True)
                    sys.exit(1)
                source_tag[attribute_name] = Path(
                    assets_dir_name, local_file_name,
                )
            bar.next()  # noqa:B305
    logger.debug('Finish downloading assets')
    return soup.prettify(formatter='html5')


def get_asset(assets_local_dir, full_asset_url, local_file_name):
    asset_content = requests.get(full_asset_url).content
    Path(assets_local_dir, local_file_name).write_bytes(asset_content)


def compose_local_name(resource_url: str, resource_type: str = '') -> str:
    """Compose a path name for a resource.

    Args:
        resource_url (str): resource url
        resource_type (str): resource type

    Returns:
        str: resource local file name
    """
    url_parse = urlparse(resource_url)
    ext = Path(url_parse.path).suffix
    pattern = rf'{ext}$'
    file_name = re.sub(pattern, '', url_parse.netloc + url_parse.path)
    file_name = re.sub(r'\W+', '-', file_name)
    if resource_type == 'dir':
        return str(file_name + '_files')  # noqa:WPS336
    return str(file_name + (ext or '.html'))
