#!/bin/sh

yes y | sudo pip3 uninstall universal-parser-tool
rm dist/*
python3 setup.py sdist bdist_wheel
sudo pip3 install dist/universal_parser_tool-0.2.4-py3-none-any.whl
