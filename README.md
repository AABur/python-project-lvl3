
# Page-loader

[![Actions Status](https://github.com/AABur/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/AABur/python-project-lvl3/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/a1d0267ab625db11610f/maintainability)](https://codeclimate.com/github/AABur/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a1d0267ab625db11610f/test_coverage)](https://codeclimate.com/github/AABur/python-project-lvl3/test_coverage)

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

[![Challenge | 100 Days of Code](https://img.shields.io/static/v1?label=Challenge&labelColor=384357&message=100%20Days%20of%20Code&color=00b4ee&style=for-the-badge&link=https://www.100daysofcode.com)](https://www.100daysofcode.com)

**Page-loader** is a command-line utility which downloads a page from the web and save it in a specified existing directory (by default in the current directory). It returns the full path to the downloaded file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **Page-loader**.

```bash
pip install --user git+https://github.com/AABur/python-project-lvl3.git
```

## Usage

### As library function

```python
from page_loader import download

file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
print(file_path)  # => '/var/tmp/ru-hexlet-io-courses.html'
```

### As CLI util

```bash
$ page-loader --output /var/tmp https://ru.hexlet.io/courses
/var/tmp/ru-hexlet-io-courses.html
```

## Usage exemple

[![asciicast](https://asciinema.org/a/Fl0mOTIghmgc3DzwD6bsex4fX.svg)](https://asciinema.org/a/Fl0mOTIghmgc3DzwD6bsex4fX?autoplay=1&speed=2&preload=1&size=medium)

## Contributing

This is a learning project and the contribution is not accepted.

## License

[MIT License](https://github.com/AABur/python-project-lvl2/blob/master/LICENSE)
