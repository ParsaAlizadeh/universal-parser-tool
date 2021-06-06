# Universal Parser Tool
[![Version](https://img.shields.io/pypi/v/universal-parser-tool?color=green)](https://pypi.org/project/universal-parser-tool/)
[![Downloads](https://pepy.tech/badge/universal-parser-tool)](https://pepy.tech/project/universal-parser-tool)
[![License](https://img.shields.io/pypi/l/universal-parser-tool)](https://github.com/ParsaAlizadeh/universal-parser-tool/blob/main/LICENSE)

This tool (a.k.a `upt`) helps to fetch sample tests from online judges.
It can be useful to speedup testing codes before final submit.

## Install

Simple and straight. Make sure you have `python3` and `pip3`. Then install using this command.

```
$ pip3 install universal-parser-tool
```

This script needs selenium to login services. The python library will be added by default if you use the above command. 
The below link has explained how to install selenium drivers.
Firefox is the default driver for this code, so install Firefox and it's driver (geckodriver) as in the link below.

https://selenium-python.readthedocs.io/installation.html

After installing, the `upt` command will be added to your PATH.

## Getting Started

All configs stored at `~/.config/upt`, including `upt.conf` (general configs) and `cookie.jar` (cookies).

After installing, first run `upt init` to initialize config files.
It will ask some questions about default settings. 

## Upgrade
You can check current version by running `upt -v`. Upgrade to newer version by this command.

```
$ pip3 install -U universal-parser-tool
```

## Parse

You can use `upt` like this script:

```
$ upt {parser}  [options...] {task or URL}
```

Parsers are listed below. You can find their options and task pattern in the repository's wiki.

## Supported Parsers

In this time, these judges have parsers.

- [AtCoder](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/AtCoder)
- [Codeforces](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Codeforces)
- [Quera](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Quera)
- [Usaco](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Usaco)

**NOTE**: You need to login a service if you want to use it during contest.

## Contributing

All contributes are welcome, specially adding new parsers.
I tried to make it easy to define your own parsers.
You can see [example.py](example/example.py) as a documented example
or [module directory](upt/) predefined parsers.