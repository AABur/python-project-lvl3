# -*- coding:utf-8 -*-
"""Creates an argument parser for the command line interface."""

import argparse


def arg_parser():
    """Create a parser for command line arguments .

    Returns:
        ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description='CLI utility to download locally pages from url provided.',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='%(prog)s 0.1.0',  # noqa: WPS323
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        dest='output_dir',
        metavar='[dir]',
        default='./',
        help='output dir (default: "./")',
    )
    parser.add_argument(
        'page_url',
        type=str,
        help='page url to download',
    )
    return parser
