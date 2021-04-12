# -*- coding:utf-8 -*-

import argparse


def arg_parser():
    parser = argparse.ArgumentParser(
        description='CLI utility that downloads pages from the internet and stores them locally.',  # noqa: E501
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
