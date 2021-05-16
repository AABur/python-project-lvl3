# -*- coding:utf-8 -*-

from pathlib import Path, PurePath

import pytest


@pytest.fixture()
def files():
    page_remote_path = Path(PurePath('tests/fixtures/remote-page.html'))
    page_local_path = Path(PurePath('tests/fixtures/local-page.html'))
    image_path = Path(PurePath('tests/fixtures/python.png'))
    link_path = Path(PurePath('tests/fixtures/application.css'))
    script_path = Path(PurePath('tests/fixtures/runtime.js'))
    return {
        'page_remote': page_remote_path.read_bytes(),
        'page_local': page_local_path.read_bytes(),
        'image': image_path.read_bytes(),
        'link': link_path.read_bytes(),
        'script': script_path.read_bytes(),
    }
