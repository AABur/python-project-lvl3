# -*- coding:utf-8 -*-

# ‘tmpdir’ fixture
# https://docs.pytest.org/en/stable/tmpdir.html#the-tmpdir-fixture

# 'requests_mock' fixture
# https://requests-mock.readthedocs.io/en/latest/pytest.html

from page_loader.download import create_file_name, download


def test_create_file_name():
    file_name = create_file_name('https://ru.hexlet.io/courses')
    assert file_name == 'ru-hexlet-io-courses.html'


def test_download(tmpdir, requests_mock):
    requests_mock.get('http://test.com', text='data')
    file_path = download('http://test.com', tmpdir)
    file_content = file_path.read_text()
    assert file_path.is_file() is True
    assert file_content == 'data'
