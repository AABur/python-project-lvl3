#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Download a page from the command line."""

# TODO: add exceptions handling for operations with files and dirs
# TODO: add exceptions handling for network errors


from page_loader import download
from page_loader.cli import arg_parser


def main():
    """Download the page ."""
    args = arg_parser().parse_args()
    print(download(args.page_url, args.output_dir))


if __name__ == '__main__':
    main()
