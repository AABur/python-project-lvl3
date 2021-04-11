# -*- coding:utf-8 -*-

from page_loader import download
from page_loader.arg_parser import arg_parser


def main():
    args = arg_parser().parse_args()
    print(download(args.page_url, args.output_dir))


if __name__ == '__main__':
    main()
