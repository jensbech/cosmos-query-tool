# Cosmos Query CLI

## Installation

```bash
pip install .
```

## Quick Start

```bash
cosmos-query -a myaccount -d mydb -c mycont -q "SELECT * FROM c" | jq
```

## Usage

### Environment Variables (Recommended)
```bash
export COSMOS_ACCOUNT="your-account"
export COSMOS_DATABASE="your-database" 
export COSMOS_CONTAINER="your-container"
export COSMOS_DB_KEY="your-key"

cosmos-query -q "SELECT * FROM c" | jq
```

### Options

```
-a, --account     Account name (or COSMOS_ACCOUNT env var)
-d, --database    Database ID (or COSMOS_DATABASE env var) 
-c, --container   Container ID (or COSMOS_CONTAINER env var)
-q, --query       SQL query (required)
-k, --key         Master key (or COSMOS_DB_KEY env var)
-o, --output      Save to file instead of stdout
--compact         No JSON indentation
--quiet           No progress messages (for piping)
-v, --verbose     Extra details
```

### Examples

Basic query:
```bash
cosmos-query -a myaccount -d mydb -c mycont -q "SELECT * FROM c"
```

With jq formatting:
```bash
cosmos-query -q "SELECT * FROM c" | jq
```

Compact output:
```bash
cosmos-query -q "SELECT * FROM c" --compact
```

Quiet mode for scripting:
```bash
cosmos-query -q "SELECT * FROM c" --quiet | jq '.[] | .name'
```

Save to file:
```bash
cosmos-query -q "SELECT * FROM c" -o results.json
```

### Get Your Cosmos DB Key

```bash
az cosmosdb keys list --name "account" --resource-group "rg" --query "primaryMasterKey" -o tsv
```

## Development

### Project Structure

```
cosmos-query-cli/
├── src/
│   └── cosmos_query/          # Main package source code
│       ├── __init__.py
│       └── cli.py
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py
│   └── test_cli.py
├── docs/                      # Documentation
│   ├── README.md
│   └── changelog.md
├── scripts/                   # Build and utility scripts
│   ├── build_binary.sh
│   ├── install.sh
│   └── README.md
├── pyproject.toml             # Project configuration
├── Makefile                   # Development commands
└── README.md
```

### Development Setup

```bash
# Install in development mode
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Run linting
make lint

# Run type checking
make typecheck

# Build binary
make binary
```

### Available Make Commands

Run `make help` to see all available development commands.
