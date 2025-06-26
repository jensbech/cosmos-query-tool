#!/bin/bash

set -e

echo "🏗️  Building standalone binary for cosmos-query..."

if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

echo "🔨 Creating binary..."
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

echo "✅ Binary created successfully!"
echo "📁 Location: dist/cosmos-query"
