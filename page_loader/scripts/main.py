#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Download a page from the command line."""

import logging
from logging.config import dictConfig

from page_loader import download
from page_loader.cli import arg_parser

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # noqa: C812, E501, WPS323
        },
    },
    'handlers': {
        'console_out': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'stream': 'ext: // sys.stdout',
        },
        'console_err': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'ERROR',
            'stream': 'ext: // sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'page-loader.log',
            'level': 'INFO',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console_out', 'console_err', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

dictConfig(logger_config)

logger = logging.getLogger(__name__)


def main():
    """Download the page."""
    logger.info('START')
    args = arg_parser().parse_args()
    print(download(args.page_url, args.output_dir))
    logger.info('FINISH')


if __name__ == '__main__':
    main()
