#!/usr/bin/env python3
import os
import sys
import argparse
from typing import Any, List, Tuple, Type


def _import_dependencies() -> Tuple[Any, Any, Any]:
    import json
    import time
    import warnings

    warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
    warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

    return json, time, warnings


def _import_azure_cosmos() -> Tuple[Any, Type[Exception], Type[Exception]]:
    try:
        import azure.cosmos.cosmos_client as cosmos_client
        from azure.cosmos.exceptions import (
            CosmosResourceNotFoundError,
            CosmosHttpResponseError,
        )

        return cosmos_client, CosmosResourceNotFoundError, CosmosHttpResponseError
    except ImportError as e:
        print_error("Failed to import Azure Cosmos DB dependencies")
        print_info(f"Error: {e}")
        print_info("Please install with: pip install azure-cosmos")
        sys.exit(1)


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def print_error(message: str) -> None:
    print(f"{Colors.RED}Error: {message}{Colors.END}", file=sys.stderr)


def print_success(message: str) -> None:
    print(f"{Colors.GREEN} {message}{Colors.END}", file=sys.stderr)


def print_info(message: str) -> None:
    print(f"{Colors.BLUE}  {message}{Colors.END}", file=sys.stderr)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query Azure Cosmos DB")

    parser.add_argument(
        "-a",
        "--account",
        help="Cosmos DB account name (or set COSMOS_ACCOUNT env var)",
        default=os.environ.get("COSMOS_ACCOUNT"),
    )

    parser.add_argument(
        "-d",
        "--database",
        help="Database ID (or set COSMOS_DATABASE env var)",
        default=os.environ.get("COSMOS_DATABASE"),
    )

    parser.add_argument(
        "-c",
        "--container",
        help="Container ID (or set COSMOS_CONTAINER env var)",
        default=os.environ.get("COSMOS_CONTAINER"),
    )

    parser.add_argument("-q", "--query", required=True, help="SQL query to execute")

    parser.add_argument(
        "-k",
        "--key",
        help="Cosmos DB master key (or set COSMOS_DB_KEY env var)",
        default=os.environ.get("COSMOS_DB_KEY"),
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    missing_args = []

    if not args.account:
        missing_args.append("Cosmos DB account name")

    if not args.database:
        missing_args.append("Database ID")

    if not args.container:
        missing_args.append("Container ID")

    if not args.key:
        missing_args.append("Cosmos DB master key")

    if missing_args:
        print_error("Missing required configuration:")
        print("", file=sys.stderr)

        for i, arg in enumerate(missing_args, 1):
            print(f"  {i}. {Colors.YELLOW}{arg}{Colors.END}", file=sys.stderr)

        print(
            f"\n{Colors.BOLD}You can provide these values in two ways:{Colors.END}",
            file=sys.stderr,
        )
        print(
            f"\n{Colors.CYAN}Option 1 - Command line arguments:{Colors.END}",
            file=sys.stderr,
        )
        if "Cosmos DB account name" in missing_args:
            print('  --account "your-account-name"', file=sys.stderr)
        if "Database ID" in missing_args:
            print('  --database "your-database-id"', file=sys.stderr)
        if "Container ID" in missing_args:
            print('  --container "your-container-id"', file=sys.stderr)
        if "Cosmos DB master key" in missing_args:
            print('  --key "your-cosmos-key"', file=sys.stderr)

        print(
            f"\n{Colors.CYAN}Option 2 - Environment variables:{Colors.END}",
            file=sys.stderr,
        )
        if "Cosmos DB account name" in missing_args:
            print('  export COSMOS_ACCOUNT="your-account-name"', file=sys.stderr)
        if "Database ID" in missing_args:
            print('  export COSMOS_DATABASE="your-database-id"', file=sys.stderr)
        if "Container ID" in missing_args:
            print('  export COSMOS_CONTAINER="your-container-id"', file=sys.stderr)
        if "Cosmos DB master key" in missing_args:
            print('  export COSMOS_DB_KEY="your-cosmos-key"', file=sys.stderr)

        if "Cosmos DB master key" in missing_args:
            print(
                f"\n{Colors.MAGENTA}To get your Cosmos DB key:{Colors.END}",
                file=sys.stderr,
            )
            print("  az cosmosdb keys list \\", file=sys.stderr)
            print('    --name "your-account-name" \\', file=sys.stderr)
            print('    --resource-group "your-resource-group" \\', file=sys.stderr)
            print('    --query "primaryMasterKey" \\', file=sys.stderr)
            print("    --output tsv", file=sys.stderr)

        print(
            f"\n{Colors.GREEN}Set required values.{Colors.END}",
            file=sys.stderr,
        )
        sys.exit(1)


def execute_query(args: argparse.Namespace) -> List[Any]:
    json, time, warnings = _import_dependencies()

    cosmos_client, CosmosResourceNotFoundError, CosmosHttpResponseError = (
        _import_azure_cosmos()
    )

    host = f"https://{args.account}.documents.azure.com:443/"

    try:
        client = cosmos_client.CosmosClient(host, {"masterKey": args.key})
        db = client.get_database_client(args.database)
        container = db.get_container_client(args.container)

        start_time = time.time()

        items = list(
            container.query_items(query=args.query, enable_cross_partition_query=True)
        )

        end_time = time.time()
        duration = end_time - start_time

        print_success(
            f"Query completed in {duration:.2f} seconds, retrieved {len(items)} items"
        )

        return items

    except CosmosResourceNotFoundError as e:
        print_error("Resource not found")
        if "database" in str(e).lower():
            print_info(
                f"Database '{args.database}' does not exist or is not accessible"
            )
        elif "container" in str(e).lower():
            print_info(
                f"Container '{args.container}' does not exist in "
                f"database '{args.database}'"
            )
        else:
            print_info(f"Details: {e}")
        sys.exit(1)
    except CosmosHttpResponseError as e:
        print_error("Cosmos DB request failed")
        if hasattr(e, "status_code"):
            if e.status_code == 401:
                print_info("Authentication failed - check your Cosmos DB key")
            elif e.status_code == 403:
                print_info("Access forbidden - check your permissions")
            elif e.status_code == 400:
                print_info("Bad request - check your query syntax")
            else:
                print_info(f"HTTP {e.status_code}: {e}")
        else:
            print_info(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print_error("Unexpected error occurred")
        print_info(f"Details: {e}")
        sys.exit(1)


def output_results(items: List[Any]) -> None:
    json, time, warnings = _import_dependencies()

    try:
        json.dump(items, sys.stdout, indent=4)
    except BrokenPipeError:
        pass


def main() -> None:
    parser = create_parser()

    if len(sys.argv) == 1:
        print_error("No arguments provided")
        print_info("A query is required to run cosmos-query")
        sys.exit(1)

    args = parser.parse_args()

    if not args.query:
        print_error("Query is required")
        sys.exit(1)

    validate_args(args)

    items = execute_query(args)

    output_results(items)


if __name__ == "__main__":
    main()
