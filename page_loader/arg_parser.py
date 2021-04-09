# -*- coding:utf-8 -*-

import argparse


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Generate difference of two JSON or YAML files.',
    )
    parser.add_argument(
        'page_url',
        type=str,
        help='page url',
    )
    parser.add_argument(
        'output_dir',
        type=str,
        default='.',
        help="output dir (default: '{0}')".format('.'),
    )
    parser.add_argument(
        '--output',
        type=str,
    )
    return parser
