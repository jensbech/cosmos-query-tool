#!/bin/bash

set -e

echo "🚀 Installing Cosmos Query CLI..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is required but not installed."
    exit 1
fi

# Install the package
echo "📦 Installing package and dependencies..."
pip3 install .

# Verify installation
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
