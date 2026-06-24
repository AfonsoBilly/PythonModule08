"""construct.py - Exercise 0: Entering the Matrix.

Detect whether the current interpreter runs inside a Python virtual
environment (the "construct") and report details about it. When run
outside a virtual environment, explain how to create and activate one.

Authorized: sys, os, site modules and print().
"""

import os
import site
import sys


def in_virtual_env() -> bool:
    """Return True when running inside a virtual environment.

    ``sys.base_prefix`` points to the Python installation a virtual
    environment was created from. Inside a venv ``sys.prefix`` is the
    venv directory, so the two prefixes differ; outside a venv they are
    identical.
    """
    return sys.prefix != sys.base_prefix


def current_site_packages() -> str:
    """Return the site-packages directory used by this interpreter.

    ``site.getsitepackages()`` returns several entries whose order is
    platform specific (on Windows the interpreter prefix comes first),
    so prefer the entry that actually ends in ``site-packages``.
    """
    if hasattr(site, "getsitepackages"):
        locations = site.getsitepackages()
        for location in locations:
            if location.endswith("site-packages"):
                return location
        if locations:
            return locations[-1]
    return site.getusersitepackages()


def report_global() -> None:
    """Print the report shown when no virtual environment is active."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def report_construct() -> None:
    """Print the report shown when a virtual environment is active."""
    env_path = sys.prefix
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(env_path)}")
    print(f"Environment Path: {env_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(current_site_packages())


def report_locations() -> None:
    """Show the difference between global and venv package locations."""
    print()
    print("Package location comparison:")
    print(f"  Global interpreter prefix: {sys.base_prefix}")
    print(f"  Active interpreter prefix: {sys.prefix}")
    if in_virtual_env():
        print("  -> Packages install into the isolated construct above.")
    else:
        print("  -> Packages install system-wide; no isolation in effect.")


def main() -> None:
    """Detect the environment and print the matching report."""
    if in_virtual_env():
        report_construct()
    else:
        report_global()
    report_locations()


if __name__ == "__main__":
    main()
