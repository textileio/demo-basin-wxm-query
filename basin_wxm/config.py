"""Configs & command setup for query start time, end time, and verbose logging."""

from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from json import load
from time import mktime
from typing import Tuple

# Define global setting for verbose traceback logging
log_traceback = True


def parse_timestamp(timestamp: str) -> int:
    """Parses a timestamp in either Unix or YYYY-MM-DD format."""
    try:
        if timestamp.isdigit():
            return int(timestamp)
        else:
            dt = datetime.strptime(timestamp, "%Y-%m-%d")
            unix_timestamp = int(mktime(dt.timetuple()))
            return unix_timestamp
    except ValueError as e:
        raise ArgumentTypeError(
            f"Invalid timestamp format: {timestamp}", e, ArgumentTypeError
        )


def command_setup() -> Tuple[int | None, int | None]:
    """
    Sets up command line argument parsing, returning the start and end
    timestamps (defaults to None if not provided). Flags include:
    - `--start`: Start timestamp for data range in unix ms (e.g., 1700438400000)
    - `--end`: End timestamp for data range in unix ms (e.g., 1700783999000)
    - `--verbose`: Enable verbose error logging with tracebacks (default: true)

    Returns:
        (int | None, int | None): The start and end timestamps.
    """
    global log_traceback

    parser = ArgumentParser(description="Fetch wxm vault data and run queries.")
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start timestamp for data range in (unix or YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End timestamp for data range in (unix or YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--verbose",
        type=int,
        default=True,
        help="Enable verbose error logging with tracebacks (default: true)",
    )

    # Parse the arguments for start and end time query ranges; also verbose logging
    # Default to `None` and let the queries use full range if no start/end
    args = parser.parse_args()
    start_raw, end_raw, log_traceback = args.start, args.end, args.verbose
    # If data in format YYYY-MM-DD, convert to unix timestamp
    start = parse_timestamp(start_raw) if start_raw else None
    end = parse_timestamp(end_raw) if end_raw else None

    return (start, end)


def get_vaults_config():
    """
    Read the vaults configuration from the `vaults.json` file.
    """
    with open("vaults-config.json", "r") as f:
        vaults_config = load(f)
        return vaults_config
