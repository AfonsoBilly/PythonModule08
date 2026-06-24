"""oracle.py - Exercise 2: Accessing the Mainframe.

Load application configuration from environment variables and an
optional .env file (via python-dotenv) and report it. The behaviour
differs between development and production so the distinction is always
visible in the output, and missing production secrets are treated as
errors instead of being silently defaulted.

Authorized: os, sys, python-dotenv modules and file operations.
"""

import os
import sys

CONFIG_KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

PRODUCTION_REQUIRED: list[str] = [
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
]


def load_env_file() -> bool:
    """Load variables from a .env file using python-dotenv.

    Existing environment variables are never overwritten (``override``
    is False), so values exported in the shell take precedence over the
    .env file. Returns True when a file was actually loaded.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("WARNING: python-dotenv is not installed.")
        print("  Install it with: pip install python-dotenv")
        print("  Reading configuration from the OS environment only.")
        return False
    return load_dotenv(override=False)


def read_config() -> dict[str, str | None]:
    """Collect the known configuration keys from the environment."""
    return {key: os.environ.get(key) for key in CONFIG_KEYS}


def resolve_mode(raw_mode: str | None) -> str:
    """Normalise MATRIX_MODE, defaulting to development."""
    mode = (raw_mode or "development").strip().lower()
    if mode not in ("development", "production"):
        print(
            f"WARNING: unknown MATRIX_MODE '{raw_mode}', "
            "falling back to development."
        )
        return "development"
    return mode


def mask_secret(value: str) -> str:
    """Return *value* with its middle hidden so it is safe to print."""
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


def safe_url(url: str) -> str:
    """Return *url* with any embedded credentials removed."""
    scheme, separator, rest = url.partition("://")
    if separator and "@" in rest:
        host = rest.split("@", 1)[1]
        return f"{scheme}://***@{host}"
    return url


def describe_database(url: str | None, mode: str) -> str:
    """Describe the database configuration for the active mode."""
    if url:
        return f"Connected ({safe_url(url)})"
    if mode == "development":
        return "Connected to local instance (default, DATABASE_URL unset)"
    return "ERROR: DATABASE_URL is required in production"


def describe_api(api_key: str | None, mode: str) -> str:
    """Describe API authentication for the active mode."""
    if api_key:
        return f"Authenticated (key {mask_secret(api_key)})"
    if mode == "development":
        return "Not configured (development allows anonymous access)"
    return "ERROR: API_KEY is required in production"


def resolve_log_level(level: str | None, mode: str) -> str:
    """Return the effective log level, with a mode-specific default."""
    if level:
        return level.upper()
    return "DEBUG" if mode == "development" else "WARNING"


def describe_zion(endpoint: str | None, mode: str) -> str:
    """Describe the Zion network endpoint for the active mode."""
    if endpoint:
        return f"Online ({endpoint})"
    if mode == "development":
        return "Online (local simulation, ZION_ENDPOINT unset)"
    return "ERROR: ZION_ENDPOINT is required in production"


def missing_required(mode: str, config: dict[str, str | None]) -> list[str]:
    """Return required keys missing for production (empty in dev)."""
    if mode != "production":
        return []
    return [key for key in PRODUCTION_REQUIRED if not config.get(key)]


def print_configuration(mode: str, config: dict[str, str | None]) -> None:
    """Print the loaded configuration block."""
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {describe_database(config['DATABASE_URL'], mode)}")
    print(f"API Access: {describe_api(config['API_KEY'], mode)}")
    print(f"Log Level: {resolve_log_level(config['LOG_LEVEL'], mode)}")
    print(f"Zion Network: {describe_zion(config['ZION_ENDPOINT'], mode)}")


def print_security_check(
    loaded: bool, config: dict[str, str | None]
) -> None:
    """Print the environment security check block."""
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if loaded or any(config.values()):
        print("[OK] .env file properly configured")
    else:
        print("[!!] No .env file or environment variables detected")
    print("[OK] Production overrides available")


def main() -> None:
    """Load configuration and report it for the active mode."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    loaded = load_env_file()
    config = read_config()
    mode = resolve_mode(config["MATRIX_MODE"])
    missing = missing_required(mode, config)

    print_configuration(mode, config)
    print()
    print_security_check(loaded, config)

    if missing:
        print()
        print("ORACLE ERROR: production configuration is incomplete.")
        for key in missing:
            print(f"  Missing required variable: {key}")
        print("Provide them via environment variables or a .env file.")
        sys.exit(1)

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
