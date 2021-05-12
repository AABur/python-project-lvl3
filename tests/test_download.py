# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

from pathlib import Path, PurePath
from urllib.parse import urljoin

import pytest

from page_loader.engine import compose_path_name, download

PAGE_URL = 'https://ru.hexlet.io/courses'


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ],
)
def test_compose_path_name_page(file_url, file_name):
    assert file_name == compose_path_name(file_url, 'page')


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-packs-js-runtime.js',
        ),
    ],
)
def test_create_file_name_full_path(file_url, file_name):
    assert file_name == generate_file_name(file_url)


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-packs-js-runtime.js',
        ),
    ],
)
def test_compose_path_name_asset_full(file_url, file_name):
    assert file_name == compose_path_name(file_url, 'asset')


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('/assets/application.css', 'ru-hexlet-io-assets-application.css'),
        (
            '/assets/professions/prof_python.png',
            'ru-hexlet-io-assets-professions-prof-python.png',
        ),
    ],
)
def test_compose_path_name_asset_relative(file_url, file_name):
    full_url = urljoin(PAGE_URL + '/', file_url)
    assert file_name == compose_path_name(full_url, 'asset')


def test_download_html(tmpdir, requests_mock):
    received_html = Path(PurePath('tests/fixtures/remote-page.html'))
    received_page = received_html.read_bytes()
    expected_html = Path(
        PurePath('tests/fixtures/remote-page.html'),
    )
    expected_page = expected_html.read_bytes()
    requests_mock.get(
        'https://ru.hexlet.io/courses',
        content=received_page,
    )
    actual_html = download(
        'https://ru.hexlet.io/courses', tmpdir,
    )
    actual_page = actual_html.read_bytes()
    assert expected_page == actual_page
