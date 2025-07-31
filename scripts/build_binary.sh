#!/bin/bash

set -e

echo "Building binary..."

if ! command -v pyinstaller &> /dev/null; then
    pip install pyinstaller
fi

pyinstaller \
    --onefile \
    --name cosmos-query \
    --console \
    --clean \
    --optimize=2 \
    --strip \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --exclude-module PIL \
    --exclude-module numpy \
    --exclude-module scipy \
    --exclude-module pandas \
    src/cosmos_query/cli.py

echo "Build complete. Binary location: dist/cosmos-query"
