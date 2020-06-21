# Universial Problem Parser Tool

## Install

Make sure that python3 is installed on your system and it is on your PATH.

This script need selenium to run. Below link has explained how to install selenium for python.
Firefox is the default driver for this code, so install Firefox and it's driver as in link below.

https://selenium-python.readthedocs.io/installation.html

The main idea is based on [this repository](https://github.com/xalanq/cf-tool).
So add `cf` file to your PATH.

For using globaly, you must add a script to your PATH. You can find a sample
bash file in `upt.example`

## Parse

You can use `upt` like this script:

`upt <PARSER> <PARSER COMMANDS>`


## Supported Parser

In this time, these judges have parsers. You can find more info about them
in their directory.

- AtCoder
- Codechef
- Spoj
- Quera

## Manual Parser

You can write your own parser for different judges.

- Create a directory named `<PARSER>` and a python file named `__init__.py` inside it.
You must write your parser in this code

- In `__init__.py` there must be a class named `Parser` and has method `get_sample`.
```python
class Parser:
    @staticmethod
    def parse(args):
        # Your Code
        return sample
```
`args` is the same as `<PARSER COMMANDS>` and it is a list of arguments passed to the parser.
It is recommended to use `logging` to output info about parser condition.

Also there are some pre-written codes in utils that can help to make your parser simpler.
For more information, read utils source or other parsers.

- Import your `<PARSER>` in `upt.py` and add the package to `PARSER` variable.

- Enjoy!
