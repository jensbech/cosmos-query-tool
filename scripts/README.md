# Build and Installation Scripts

This directory contains scripts for building and installing the Cosmos Query CLI tool.

## Scripts

### `build_binary.sh`
Builds a standalone binary using PyInstaller. This allows the tool to be distributed as a single executable file without requiring Python to be installed on the target system.

### `install.sh`
Installation script for setting up the development environment and installing dependencies.

## Usage

### Building a Binary
```bash
./scripts/build_binary.sh
```

### Installing for Development
```bash
./scripts/install.sh
```

## Requirements

- Python 3.8 or higher
- pip
- virtualenv (recommended)

For binary building:
- PyInstaller
- All project dependencies
