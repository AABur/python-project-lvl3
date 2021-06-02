#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Download a page from the command line."""


import logging

from page_loader import download
from page_loader.cli import arg_parser

logger = logging.getLogger('page-loader')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('page-loader.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',   # noqa:WPS323
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def main():
    """Download the page."""
    logger.info('START')
    args = arg_parser().parse_args()
    print(download(args.page_url, args.output_dir))
    logger.info('FINISH')


if __name__ == '__main__':
    main()
