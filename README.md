# Universal Problem Parser Tool

## Install

Simple and straight. Make sure you have Python3 and pip. Then install using this command.

`pip install universal-parser-tool`

This script needs selenium to run. This python library will be added by default if you use the above command. 
The below link has explained how to install selenium drivers.
Firefox is the default driver for this code, so install Firefox and it's driver (geckodriver) as in the link below.

https://selenium-python.readthedocs.io/installation.html

The main idea is based on [this repository](https://github.com/xalanq/cf-tool).
So you may add `cf` to your PATH.

After installing, the `upt` command will be added to your PATH.

## Configuration

The config file located in `~/.uptrc`. Some data may be stored here from parsers too.

After installing, initialize the root path using this command:

`upt init <ROOT>`

Some parsers create their tests in the root. For example, if `<ROOT>=~/cf/contest` and run `upt cf 4A`,
then test files will be available in `~/cf/contest/4/A`. 

## Parse

You can use `upt` like this script:

`upt <PARSER> <PARSER COMMANDS>`

Parsers are listed below. You can find their commands in the repository's wiki.

## Supported Parsers

In this time, these judges have parsers.

- [AtCoder](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/AtCoder) (+login)
- [Codechef](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Codechef)
- [Codeforces](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Codeforces)
- [Quera](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Quera) (+login)
- [Spoj](https://github.com/ParsaAlizadeh/universal-parser-tool/wiki/Spoj)

**NOTE**: You may use the parser for practice problems. During a contest, some judges need to log in.
For now, this feature is supported by parsers with (+login).
