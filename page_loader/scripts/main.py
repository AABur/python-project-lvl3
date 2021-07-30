#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Download a page from the command line."""

import logging

from page_loader import download
from page_loader.cli import arg_parser

logger_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters':
        {
            'default':
            {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # noqa: C812, E501, WPS323
            },
        },
    'handlers':
        {
            'console':
            {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'INFO',
            },
            'file':
            {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': 'page-loader.log',
                'level': 'DEBUG',
            },
        },
    'loggers':
        {
            'page-loader':
            {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
}

logging.coding.dictConfig(logger_config)

logger = logging.getLogger(__name__)


def main():
    """Download the page."""
    logger.info('START')
    args = arg_parser().parse_args()
    print(download(args.page_url, args.output_dir))
    logger.info('FINISH')


if __name__ == '__main__':
    main()
