# -*- coding:utf-8 -*-

from page_loader import download


def test_file_path():
    file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
    assert file_path == '/var/tmp/ru-hexlet-io-courses.html'
