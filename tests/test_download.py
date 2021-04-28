# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

import pytest
from pathlib import PurePath

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


def test_download_img(tmpdir, requests_mock):
    requested_img_file = PurePath('tests/fixtures/received/prof_python.png')
    expected_img_file = PurePath(
        'tests/fixtures/expected/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-prof-python.png',  # noqa E501
    )
    requests_mock.get(
        '/assets/professions/prof_python.png',
        content=requested_img_file,
    )
    file_path = download(
        'https://ru.hexlet.io/assets/professions/prof_python.png', tmpdir,
    )
    file_content = file_path.read_text()
    assert expected_img_file == requested_img_file
