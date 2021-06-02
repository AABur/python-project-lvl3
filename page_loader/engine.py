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
    page_file_path = Path(Path.cwd(), target_dir, local_page_name)
    assets_dir_path = Path(Path.cwd(), target_dir, assets_dir_name)
    logger.debug(
        'Start downloading {0} to {1}'.format(page_url, page_file_path))
    logger.debug('111')
    try:
        Path(assets_dir_path).mkdir(exist_ok=True)
    except Exception:
        logger.error('Failed to mkdir', exc_info=True)
        sys.exit(1)
    # collect remote assets and prepare local html-page
    logger.debug('222')
    try:
        local_html = fetch_assets(
            page_url,
            assets_dir_name,
            assets_dir_path,
        )
    except Exception:
        logger.error('Failed to fetch_assets', exc_info=True)
        sys.exit(1)
    logger.debug('333')
    try:
        Path(page_file_path).write_text(local_html)  # save html-page locally
    except Exception:
        logger.error('Failed to write file', exc_info=True)
        sys.exit(1)
    logger.debug('Finish downloading {0} to {1}'.format(
        page_url, page_file_path,
    ))
    return str(page_file_path)


def fetch_assets(
    page_url: str,
    assets_dir_name: str,
    assets_path: Path,
) -> Any:  # bs4 don't have type stub
    """Download assets from given HTML page and store it in assets directory.

    Args:
        page_url (str): given HTML page url
        assets_dir_name (str): assets directory
        assets_path (Path): [description]

    Returns:
        Any: [description]
    """
    logger.debug('Start downloading assets')
    soup = BeautifulSoup(requests.get(page_url).text, 'lxml')
    tags_list = soup.find_all(TAGS)
    bar = IncrementalBar(
        'Downloading',
        max=len(tags_list),
        suffix='%(percent).1f%% [%(elapsed)ds]',  # noqa:WPS323
    )
    if not page_url.endswith('/'):
        page_url = '{0}/'.format(page_url)

    for source_tag in tags_list:
        attribute_name = 'src' if source_tag.name in {
            'script', 'img',
        } else 'href'
        asset_url = source_tag.get(attribute_name)
        if not asset_url:
            bar.next()
            continue
        full_asset_url = urljoin(page_url, asset_url)
        logger.debug(full_asset_url)
        if urlparse(full_asset_url).netloc == urlparse(page_url).netloc:
            local_file_name = compose_local_name(full_asset_url)
            full_asset_path = Path(assets_path, local_file_name)
            logger.debug('Start downloading assets {0}'.format(full_asset_url))
            try:
                asset_content = requests.get(
                    full_asset_url, stream=True,
                ).content
            except Exception:
                logger.error('Failed to access to asset', exc_info=True)
                sys.exit(1)
            logger.debug('555')
            try:
                Path(full_asset_path).write_bytes(asset_content)
            except Exception:
                logger.error('Failed to write asset file', exc_info=True)
                sys.exit(1)
            source_tag[attribute_name] = Path(assets_dir_name, local_file_name)
        bar.next()
    bar.finish()
    logger.debug('Finish downloading assets')
    return soup.prettify(formatter='html5')


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
    file_name = (url_parse.netloc + url_parse.path).removesuffix(ext)
    file_name = re.sub(r'\W+', '-', file_name)
    if resource_type == 'dir':
        return str(file_name + '_files')  # noqa:WPS336
    return str(file_name + (ext or '.html'))
