# -*- coding:utf-8 -*-
"""Download content of the given HTML file and save it to specified directory.

Returns:
    str: saved HTML page path
"""

import logging
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.resources import fetch_resources, is_local_resource

logger = logging.getLogger('page-loader')

TAGS = ('link', 'script', 'img')


def download(page_url: str, target_dir: str = '') -> str:
    """Download a page from a page.

    Args:
        page_url (str): url to download
        target_dir (str): [optional] [defaults = ''] target directory.

    Returns:
        str: saved HTML page path
    """
    resources_dir_name = compose_local_path_name(page_url, is_dir=True)
    page_file_path = Path(target_dir, compose_local_path_name(page_url))
    logger.debug(f'Start downloading {page_url} to {page_file_path}')
    html_page = fetch_html_page(page_url)
    local_html, resources = prepare_soup(html_page, page_url, resources_dir_name)  # noqa: E501
    fetch_resources(resources, Path(target_dir, resources_dir_name))
    Path(page_file_path).write_text(local_html)
    logger.debug(f'Finish downloading {page_url} to {page_file_path}')
    return str(page_file_path)


def fetch_html_page(page_url: str) -> str:
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception('Status code = {}'.format(response.status_code))
    return response.text


def prepare_soup(html_page: str, page_url: str, resources_dir_name: str) -> Any:  # noqa: WPS210, E501
    """Prepare the HTML for the given HTML page .

    Args:
        html_page (str): HTML text
        page_url (str): page url
        resources_dir_name (str): dir name for the page resources

    Returns:
        local_html_page (str): HTML page with replaced resources file names
        resources (dict): dict with resircers urls matched to local files
    """
    soup = BeautifulSoup(html_page, 'html.parser')
    resources = {}
    for source_tag in soup.find_all(TAGS):
        attribute_name = get_attribute_ref(source_tag.name)
        full_resource_url = urljoin(page_url, source_tag.get(attribute_name))
        if is_local_resource(page_url, full_resource_url):
            local_file_name = compose_local_path_name(full_resource_url)
            resources[full_resource_url] = local_file_name
            source_tag[attribute_name] = Path(
                resources_dir_name, local_file_name,
            )
    local_html_page = soup.prettify(formatter='html5')
    return local_html_page, resources


def get_attribute_ref(tag_name):
    attribute_ref = {
        'script': 'src',
        'img': 'src',
    }
    return attribute_ref.get(tag_name, 'href')


def compose_local_path_name(resource_url: str, is_dir: bool = False) -> str:
    """Compose a path name for a resource.

    Args:
        resource_url (str): resource url
        is_dir (bool): resource type

    Returns:
        str: resource local file name
    """
    parsed_url = urlparse(resource_url)
    ext = Path(parsed_url.path).suffix
    full_path = Path(parsed_url.netloc + parsed_url.path)
    name = re.sub(
        r'\W+',
        '-',
        str(full_path.with_suffix('')),
    )
    if is_dir:
        return '{0}_files'.format(name)
    return '{0}{1}'.format(name, (ext or '.html'))
