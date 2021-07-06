# Universal Parser Tool
[![Version](https://img.shields.io/pypi/v/universal-parser-tool?color=green)](https://pypi.org/project/universal-parser-tool/)
[![Downloads](https://pepy.tech/badge/universal-parser-tool)](https://pepy.tech/project/universal-parser-tool)
[![License](https://img.shields.io/pypi/l/universal-parser-tool)](https://github.com/ParsaAlizadeh/universal-parser-tool/blob/main/LICENSE)

This tool (a.k.a `upt`) helps to fetch sample tests from online judges.
It can be useful to speedup testing codes before final submit.

## Install

You can install `upt` from pypi using this command:

```
$ pip install universal-parser-tool
```

You should be able to run `upt` after install.

To login services and use parsers on private webpages, you need to install a supported browser and its driver.

|Browser|Driver|Supported|Tested|
|:-----:|:-----|:-------:|:----:|
|Firefox|https://github.com/mozilla/geckodriver/releases|✅|✅|
|Chromium/Chrome|https://sites.google.com/a/chromium.org/chromedriver/downloads|✅|✅|
|Opera|https://github.com/operasoftware/operachromiumdriver/releases|✅|❌|
|Edge|https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/|✅|❌|
|Safari|Built-in|✅|❌|
|IE|https://selenium-release.storage.googleapis.com/index.html|❌|❌|

## Configurations

All configurations stored at `~/.config/upt`, including `upt.conf` (general configs) and `cookie.jar` (login cookies).

After installing, You may run `upt init` to initialize config options.

## Upgrade
You can check current version by running `upt -v`. Upgrade to newer version by this command.

```
$ pip install -U universal-parser-tool
```

## Parsers

At this time, these judges have parsers.

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
