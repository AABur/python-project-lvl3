# -*- coding:utf-8 -*-
"""Download the content of the given HTML file and return the content.

Returns:
    str: local HTML page
"""

import logging
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='page_loader.log',
    filemode='w',
)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


TAGS = {  # noqa:WPS407
    'link': 'href',
    'script': 'src',
    'img': 'src',
}


def download(page_url: str, target_dir: str = '') -> str:
    """Download the given url to the given path .

    Args:
        page_url (str): page url
        target_dir (str): target dir. Defaults to '.'

    Returns:
        str: local HTML file full path
    """
    local_page_name = compose_path_name(page_url, 'page')
    assets_dir_name = compose_path_name(page_url, 'dir')
    page_file_path = Path(Path(Path.cwd(), target_dir), local_page_name)
    assets_dir_path = Path(Path(Path.cwd(), target_dir), assets_dir_name)
    logger.info('Start downloading {page_url} to {target_dir}'.format(
        page_url=page_url, target_dir=page_file_path),
    )
    try:
        Path(assets_dir_path).mkdir(exist_ok=True)
    except Exception as exc:
        logger.error(exc)
        sys.exit(1)
    # collect remote assets and preapre local html-page
    local_html = fetch_assets(
        requests.get(page_url).text,
        page_url,
        assets_dir_name,
        assets_dir_path,
    )
    try:
        Path(page_file_path).write_text(local_html)  # save html-page locally
    except Exception as exc:
        logger.error(exc)
        sys.exit(1)
    logger.info('Finish downloading {page_url} to {target_dir}'.format(
        page_url=page_url, target_dir=page_file_path),
    )
    return str(page_file_path)


def fetch_assets(html_page: str, page_url: str, assets_dir_name: str, assets_path: Path) -> Any:   # noqa: E501  # FIXME assign specific type
    """Fetches the assets from the given page URL and saves it in the assets_dir .

    Args:
        html_page (str): html page
        page_url (str): html page url
        assets_dir_name (str): dir for store page
        assets_path (Path): local dir for assets

    Returns:
        Any: local HTML file
    """
    logger.info('Start downloading assets')
    soup = BeautifulSoup(html_page, 'lxml')
    tags_list = soup.find_all(TAGS.keys())
    for source_tag in tags_list:
        attribute_name = TAGS.get(source_tag.name)
        asset_url = source_tag.get(attribute_name)
        if not asset_url:
            continue
        full_asset_url = urljoin(page_url + '/', asset_url)
        if urlparse(full_asset_url).netloc == urlparse(page_url).netloc:
            local_file_name = compose_path_name(full_asset_url, 'asset')
            full_asset_path = Path(assets_path, local_file_name)
            logger.debug(
                'Start downloading assets {full_asset_url}'.format(full_asset_url=full_asset_url))
            asset_content = requests.get(full_asset_url, stream=True).content
            try:
                Path(full_asset_path).write_bytes(asset_content)
            except Exception as exc:
                logger.error(exc)
                sys.exit(1)
            source_tag[attribute_name] = Path(assets_dir_name, local_file_name)
    logger.info('Finish downloading assets')
    return soup.prettify(formatter='html5')


def compose_path_name(resource_url: str, resource_type: str) -> str:
    """Compose a path name for a resource.

    Args:
        resource_url (str): resource url
        resource_type (str): resource type

    Returns:
        str: resource local file name
    """
    url_parse = urlparse(resource_url)
    path, ext = os.path.splitext(url_parse.path)  # FIXME use pathlib instaed
    file_path = url_parse.netloc + path
    file_name = re.sub(r'\W+', '-', file_path)
    # FIXME need refactoring
    if resource_type == 'asset':
        path_ext = ext or '.html'
        return str(file_name + path_ext)
    elif resource_type == 'dir':
        return str(file_name + '_files')
    elif resource_type == 'page':
        return str(file_name + '.html')
    return ''
