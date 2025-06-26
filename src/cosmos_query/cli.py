#!/usr/bin/env python3
import os
import sys
import argparse
from typing import Optional, Any, List, Tuple, Type


def _import_dependencies() -> Tuple[Any, Any, Any]:
    import json
    import time
    import warnings

    # Suppress urllib3 warnings
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
    print(f"{Colors.RED}❌ Error: {message}{Colors.END}", file=sys.stderr)


def print_success(message: str) -> None:
    print(f"{Colors.GREEN}✅ {message}{Colors.END}", file=sys.stderr)


def print_info(message: str) -> None:
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}", file=sys.stderr)


def print_warning(message: str) -> None:
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}", file=sys.stderr)


def print_progress(message: str) -> None:
    print(f"{Colors.CYAN}🔄 {message}{Colors.END}", file=sys.stderr)


def print_header(message: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 {message}{Colors.END}", file=sys.stderr)


def show_spinner(duration: float = 1.0) -> None:
    json, time, warnings = _import_dependencies()

    spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(
            f"\r{Colors.CYAN}{spinner_chars[i % len(spinner_chars)]}{Colors.END}",
            end="",
            flush=True,
            file=sys.stderr,
        )
        time.sleep(0.1)
        i += 1
    print("\r", end="", flush=True, file=sys.stderr)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query Azure Cosmos DB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --account myaccount --database mydb --container mycont \\
           --query "SELECT * FROM c"
  %(prog)s -a myaccount -d mydb -c mycont -q "SELECT * FROM c" | jq
  %(prog)s --account myaccount --database mydb --container mycont \\
           --query "SELECT * FROM c" > results.json
  %(prog)s --account myaccount --database mydb --container mycont \\
           --query "SELECT * FROM c" --compact
  %(prog)s --account myaccount --database mydb --container mycont \\
           --query "SELECT * FROM c" --quiet | jq '.[] | .name'

Environment Variables:
  COSMOS_DB_KEY    - Cosmos DB master key (alternative to --key)
  COSMOS_ACCOUNT   - Cosmos DB account name (alternative to --account)
  COSMOS_DATABASE  - Database ID (alternative to --database)
  COSMOS_CONTAINER - Container ID (alternative to --container)
        """,
    )

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

    parser.add_argument(
        "-o", "--output", help="Output JSON file (default: print to stdout)"
    )

    parser.add_argument(
        "--host",
        help="Custom Cosmos DB host URL (default: auto-generated from account)",
    )

    parser.add_argument(
        "--cross-partition",
        action="store_true",
        default=True,
        help="Enable cross-partition query (default: True)",
    )

    parser.add_argument(
        "--no-cross-partition",
        action="store_true",
        help="Disable cross-partition query",
    )

    parser.add_argument(
        "--indent", type=int, default=4, help="JSON output indentation (default: 4)"
    )

    parser.add_argument(
        "--compact", action="store_true", help="Compact JSON output (no indentation)"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages (useful for piping output)",
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
        print_header("Configuration Error")
        print_error("Missing required configuration:")
        print("", file=sys.stderr)

        for i, arg in enumerate(missing_args, 1):
            print(f"  {i}. {Colors.YELLOW}{arg}{Colors.END}", file=sys.stderr)

        print(
            f"\n{Colors.BOLD}💡 You can provide these values in two ways:{Colors.END}",
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
                f"\n{Colors.MAGENTA}📋 To get your Cosmos DB key:{Colors.END}",
                file=sys.stderr,
            )
            print("  az cosmosdb keys list \\", file=sys.stderr)
            print('    --name "your-account-name" \\', file=sys.stderr)
            print('    --resource-group "your-resource-group" \\', file=sys.stderr)
            print('    --query "primaryMasterKey" \\', file=sys.stderr)
            print("    --output tsv", file=sys.stderr)

        print(
            f"\n{Colors.GREEN}📖 For more examples, run: "
            f"cosmos-query --help{Colors.END}",
            file=sys.stderr,
        )
        sys.exit(1)


def build_host_url(account: str, custom_host: Optional[str] = None) -> str:
    if custom_host:
        return custom_host
    return f"https://{account}.documents.azure.com:443/"


def execute_query(args: argparse.Namespace) -> List[Any]:
    json, time, warnings = _import_dependencies()

    cosmos_client, CosmosResourceNotFoundError, CosmosHttpResponseError = (
        _import_azure_cosmos()
    )

    host = build_host_url(args.account, args.host)

    if not args.quiet:
        print_header("Cosmos DB Query Execution")

        print_info(f"Account: {Colors.BOLD}{args.account}{Colors.END}")
        print_info(f"Database: {Colors.BOLD}{args.database}{Colors.END}")
        print_info(f"Container: {Colors.BOLD}{args.container}{Colors.END}")
        print_info(f"Host: {Colors.BOLD}{host}{Colors.END}")

        if args.verbose:
            print_info(f"Query: {Colors.BOLD}{args.query}{Colors.END}")
        else:
            query_preview = (
                args.query[:100] + "..." if len(args.query) > 100 else args.query
            )
            print_info(f"Query: {Colors.BOLD}{query_preview}{Colors.END}")

    try:
        if not args.quiet:
            print_progress("Connecting to Cosmos DB...")
            show_spinner(0.5)

        client = cosmos_client.CosmosClient(host, {"masterKey": args.key})
        if not args.quiet:
            print_success("Connected to Cosmos DB")

        if not args.quiet:
            print_progress("Accessing database...")
            show_spinner(0.3)
        db = client.get_database_client(args.database)
        if not args.quiet:
            print_success(f"Database '{args.database}' accessed")

        if not args.quiet:
            print_progress("Accessing container...")
            show_spinner(0.3)
        container = db.get_container_client(args.container)
        if not args.quiet:
            print_success(f"Container '{args.container}' accessed")

        cross_partition = args.cross_partition and not args.no_cross_partition

        if not args.quiet:
            if cross_partition:
                print_info("Cross-partition query: Enabled")
            else:
                print_warning("Cross-partition query: Disabled")

        if not args.quiet:
            print_progress("Executing query...")
        start_time = time.time()

        items = list(
            container.query_items(
                query=args.query, enable_cross_partition_query=cross_partition
            )
        )

        end_time = time.time()
        duration = end_time - start_time

        if not args.quiet:
            print_success(f"Query completed in {duration:.2f} seconds")
            print_success(f"Retrieved {Colors.BOLD}{len(items)}{Colors.END} items")

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
        if args.verbose:
            import traceback

            print(f"\n{Colors.RED}Full traceback:{Colors.END}")
            traceback.print_exc()
        sys.exit(1)


def output_results(
    items: List[Any],
    output_file: Optional[str],
    indent: Optional[int],
    verbose: bool = False,
    quiet: bool = False,
    compact: bool = False,
) -> None:
    json, time, warnings = _import_dependencies()

    if compact:
        indent = None

    if output_file:
        if not quiet:
            print_header("Saving Results")

            if not items:
                print_warning("No results to save")
                print_info(
                    f"Creating empty file: {Colors.BOLD}{output_file}{Colors.END}"
                )
            else:
                print_progress(f"Writing {len(items)} items to file...")

        try:
            if not quiet:
                show_spinner(0.5)

            with open(output_file, "w") as f:
                json.dump(items, f, indent=indent)

            if not quiet:
                file_size = os.path.getsize(output_file)
                file_size_mb = file_size / (1024 * 1024)

                print_success(
                    f"Results saved to: {Colors.BOLD}{output_file}{Colors.END}"
                )

                if file_size_mb > 1:
                    print_info(
                        f"File size: {Colors.BOLD}{file_size_mb:.2f} MB{Colors.END}"
                    )
                else:
                    file_size_kb = file_size / 1024
                    print_info(
                        f"File size: {Colors.BOLD}{file_size_kb:.1f} KB{Colors.END}"
                    )

                if verbose and items:
                    print_info(
                        f"JSON indentation: {indent if indent else 'compact'} spaces"
                    )

                    if len(items) > 0:
                        print_info("Preview of first result:")
                        preview = json.dumps(items[0], indent=2)
                        if len(preview) > 300:
                            preview = preview[:300] + "..."
                        print(f"{Colors.WHITE}{preview}{Colors.END}", file=sys.stderr)

                print(
                    f"\n{Colors.GREEN}🎉 Query execution completed "
                    f"successfully!{Colors.END}",
                    file=sys.stderr,
                )

        except IOError as e:
            print_error(f"Failed to write to file '{output_file}'")
            print_info(f"Details: {e}")

            if "Permission denied" in str(e):
                print_info(
                    "💡 Try running with appropriate permissions or "
                    "choose a different output location"
                )
            elif "No such file or directory" in str(e):
                print_info("💡 Make sure the directory exists or use a different path")

            sys.exit(1)
    else:
        if not quiet and verbose:
            print_header("Output Results")
            if not items:
                print_warning("No results found")
            else:
                print_info(f"Outputting {len(items)} items to stdout")
            print_info("💡 Tip: Pipe to jq for formatting: cosmos-query ... | jq")
            print_info("💡 Tip: Save to file: cosmos-query ... > results.json")
            print("", file=sys.stderr)

        try:
            json.dump(items, sys.stdout, indent=indent)
        except BrokenPipeError:
            pass

        if not quiet and verbose:
            print(
                f"\n{Colors.GREEN}🎉 Query execution completed "
                f"successfully!{Colors.END}",
                file=sys.stderr,
            )


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        parser = create_parser()
        parser.print_help()
        sys.exit(0)

    parser = create_parser()

    if len(sys.argv) == 1:
        print_error("No arguments provided!")
        print_info("A query is required to run cosmos-query.")
        print_info(
            f"Run: {Colors.BOLD}cosmos-query --help{Colors.END} for usage information"
        )
        print_info(
            f'Quick example: {Colors.BOLD}cosmos-query -q "SELECT * FROM c" '
            f"-a myaccount -d mydb -c mycontainer{Colors.END}"
        )
        sys.exit(1)

    args = parser.parse_args()

    if not args.query:
        print_error("Query is required!")
        print_info(
            f'Use: {Colors.BOLD}-q "SELECT * FROM c"{Colors.END} or '
            f'{Colors.BOLD}--query "SELECT * FROM c"{Colors.END}'
        )
        print_info(
            f"Run: {Colors.BOLD}cosmos-query --help{Colors.END} for more information"
        )
        sys.exit(1)

    validate_args(args)

    items = execute_query(args)

    output_results(
        items, args.output, args.indent, args.verbose, args.quiet, args.compact
    )


if __name__ == "__main__":
    main()
