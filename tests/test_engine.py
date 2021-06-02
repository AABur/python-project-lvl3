# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

from pathlib import Path, PurePath
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import pytest

from page_loader.engine import compose_local_name, download

PAGE_URL = 'https://ru.hexlet.io/courses'


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
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
    full_url = urljoin(PAGE_URL + '/', file_url)
    assert file_name == compose_local_name(full_url, 'asset')


def test_download_html(tmpdir, requests_mock, files):

    requests_mock.get(
        'https://ru.hexlet.io/courses',
        content=files['page_remote'],
    )
    requests_mock.get(
        '/assets/professions/python.png',
        content=files['image'],
    )
    requests_mock.get(
        '/assets/application.css',
        content=files['link'],
    )
    requests_mock.get(
        'https://ru.hexlet.io/packs/js/runtime.js',
        content=files['script'],
    )

    actual_html = download(
        'https://ru.hexlet.io/courses', tmpdir,
    )
    actual_page = Path(PurePath(actual_html)).read_bytes()
    expected_page = files['page_local']
    apb = BeautifulSoup(actual_page, 'lxml').prettify(formatter='html5')
    epb = BeautifulSoup(expected_page, 'lxml').prettify(formatter='html5')
    assert epb == apb
