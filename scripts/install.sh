#!/bin/bash

set -e

echo "🚀 Installing Cosmos Query CLI..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is required but not installed."
    exit 1
fi

echo "📦 Installing package and dependencies..."
pip3 install .

if command -v cosmos-query &> /dev/null; then
    echo "✅ Installation successful!"
    echo ""
    echo "🎉 You can now use the 'cosmos-query' command."
    echo ""
    echo "📚 For help, run: cosmos-query --help"
    echo "📖 For examples, see: README.md"
else
    echo "❌ Installation failed. The 'cosmos-query' command is not available."
    exit 1
fi
