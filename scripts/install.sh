#!/bin/bash

set -e

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed."
    exit 1
fi

pip3 install .

if command -v cosmos-query &> /dev/null; then
    echo "Installation successful"
else
    echo "Installation failed"
    exit 1
fi
