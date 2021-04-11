# -*- coding:utf-8 -*-

from page_loader.download import create_file_name, download


def test_create_file_name():
    file_name = create_file_name('https://ru.hexlet.io/courses')
    assert file_name == 'ru-hexlet-io-courses.html'


def test_create_name():
    file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
    assert str(file_path) == '/var/tmp/ru-hexlet-io-courses.html'
