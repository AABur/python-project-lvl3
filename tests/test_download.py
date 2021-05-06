# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

from pathlib import Path, PurePath

import pytest

from page_loader.download import create_file_name, download


@pytest.mark.parametrize(
    'file_url, file_name',
    [
        ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
        ('/assets/application.css', 'ru-hexlet-io-assets-application.css'),
        (
            '/assets/professions/prof_python.png',
            'ru-hexlet-io-assets-professions-prof-python.png',
        ),
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-packs-js-runtime.js',
        ),
    ],
)
def test_create_file_name(file_url, file_name):
    created_file_name = create_file_name(file_url)
    assert file_name == created_file_name


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


def test_download_img(tmpdir, requests_mock):
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
