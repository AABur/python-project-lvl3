# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

from pathlib import Path, PurePath
from urllib.parse import urljoin

import pytest
import requests
from bs4 import BeautifulSoup  # type: ignore

from page_loader.engine import compose_local_name, download

PAGE_URL = 'https://ru.hexlet.io/courses'


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        (PAGE_URL, 'ru-hexlet-io-courses.html'),
    ],
)
def test_compose_path_name_page(file_url, file_name):
    assert file_name == compose_local_name(file_url, 'page')


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('/assets/application.css', 'ru-hexlet-io-assets-application.css'),
        (
            '/assets/professions/python.png',
            'ru-hexlet-io-assets-professions-python.png',
        ),
    ],
)
def test_compose_path_name_asset_relative(file_url, file_name):
    full_url = urljoin(PAGE_URL + '/', file_url)  # noqa:WPS336
    assert file_name == compose_local_name(full_url, 'asset')


def test_download_html(tmpdir, requests_mock, files):

    requests_mock.get(PAGE_URL, content=files['page_remote'])
    requests_mock.get('/assets/professions/python.png', content=files['image'])
    requests_mock.get('/assets/application.css', content=files['link'])
    requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js', content=files['script'])  # noqa:E501

    actual_html = download(PAGE_URL, tmpdir)
    actual_page = Path(PurePath(actual_html)).read_bytes()
    expected_page = files['page_local']
    apb = BeautifulSoup(actual_page, 'lxml').prettify(formatter='html5')
    epb = BeautifulSoup(expected_page, 'lxml').prettify(formatter='html5')
    assert epb == apb


@pytest.mark.parametrize(
    'exception',
    [
        (requests.exceptions.ConnectTimeout),
        (requests.exceptions.ConnectionError),
        (requests.exceptions.HTTPError),
    ],
)
def test_network_exceptions(requests_mock, tmpdir, exception):
    requests_mock.get(PAGE_URL, exc=exception)
    with pytest.raises(Exception):
        download(PAGE_URL, tmpdir)


@pytest.mark.parametrize('status_code', [
    400, 401, 403, 404, 500, 502,
])
def test_http_status(requests_mock, tmpdir, status_code):
    requests_mock.get(PAGE_URL, status_code=status_code)
    with pytest.raises(Exception):
        download(PAGE_URL, tmpdir)


def test_os_error(tmpdir):
    tempdir = Path(tmpdir)
    tempdir.chmod(0o444)
    with pytest.raises(Exception):
        download(PAGE_URL, tempdir)
