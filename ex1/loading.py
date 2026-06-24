"""loading.py - Exercise 1: Loading Programs.

A small data-analysis tool that demonstrates package management with
both pip and Poetry. The simulated "Matrix data" is generated with
numpy, manipulated with pandas and visualised with matplotlib.

Dependencies are checked at runtime so the program degrades gracefully
when a library is missing, printing how to install it with either pip
or Poetry.

Authorized: pandas, requests, matplotlib, numpy, sys, importlib.
"""

import importlib.metadata
import importlib.util
import sys

REQUIRED_PACKAGES: list[tuple[str, str]] = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
    ("matplotlib", "Visualization"),
]

OPTIONAL_PACKAGES: list[tuple[str, str]] = [
    ("requests", "Network access"),
]

OUTPUT_FILE = "matrix_analysis.png"
DATA_POINTS = 1000


def package_version(name: str) -> str | None:
    """Return the installed version of *name*, or None if it is absent."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def is_available(module_name: str) -> bool:
    """Return True when *module_name* can be imported."""
    return importlib.util.find_spec(module_name) is not None


def check_dependencies() -> bool:
    """Print the status of every dependency.

    Returns True only when all *required* packages are importable.
    """
    print("Checking dependencies:")
    all_ready = True
    for name, description in REQUIRED_PACKAGES:
        version = package_version(name)
        if version is not None and is_available(name):
            print(f"[OK] {name} ({version}) - {description} ready")
        else:
            print(f"[MISSING] {name} - {description} unavailable")
            all_ready = False
    for name, description in OPTIONAL_PACKAGES:
        version = package_version(name)
        if version is not None and is_available(name):
            print(f"[OK] {name} ({version}) - {description} ready")
        else:
            print(f"[--] {name} - {description} (optional, not loaded)")
    return all_ready


def print_install_help() -> None:
    """Explain how to load the missing programs with pip or Poetry."""
    print()
    print("LOADING FAILED: required programs are missing.")
    print("Load them into your environment with one of:")
    print()
    print("  With pip:")
    print("    pip install -r requirements.txt")
    print("    python loading.py")
    print()
    print("  With Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py")


def compare_package_managers() -> None:
    """Show installed versions and contrast pip with Poetry."""
    print()
    print("Package manager comparison (pip vs Poetry):")
    print(f"  {'Package':<12}Installed version")
    print(f"  {'-' * 12}{'-' * 17}")
    for name, _ in REQUIRED_PACKAGES + OPTIONAL_PACKAGES:
        version = package_version(name) or "not installed"
        print(f"  {name:<12}{version}")
    print()
    print("  pip    : installs the flat list in requirements.txt;")
    print("           you pin versions by hand, no lock file.")
    print("  Poetry : reads pyproject.toml, resolves the whole")
    print("           dependency graph and writes poetry.lock for")
    print("           reproducible installs on every machine.")


def run_analysis() -> None:
    """Generate, analyse and visualise the simulated Matrix data.

    The heavy imports happen here, behind a guard: a package may be
    listed as present yet still fail to import (for example a compiled
    extension blocked by the operating system), and that must not crash
    the program with a raw traceback.
    """
    try:
        import numpy as np
        import pandas as pd  # type: ignore[import-untyped]
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as error:
        print()
        print("LOADING ERROR: a program is installed but failed to load:")
        print(f"  {error}")
        print_install_help()
        sys.exit(1)

    print()
    print("Analyzing Matrix data...")

    rng = np.random.default_rng(seed=42)
    time = np.arange(DATA_POINTS)
    drift = np.cumsum(rng.normal(0.0, 1.0, DATA_POINTS))
    pulse = 8.0 * np.sin(time / 50.0)
    noise = rng.normal(0.0, 2.0, DATA_POINTS)
    signal = drift + pulse + noise

    frame = pd.DataFrame({"time": time, "signal": signal})
    frame["rolling_mean"] = frame["signal"].rolling(window=20).mean()

    print(f"Processing {len(frame)} data points...")
    print(
        f"  mean={frame['signal'].mean():.2f} "
        f"std={frame['signal'].std():.2f} "
        f"min={frame['signal'].min():.2f} "
        f"max={frame['signal'].max():.2f}"
    )

    print("Generating visualization...")
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.plot(
        frame["time"], frame["signal"],
        color="#00ff41", linewidth=0.8, label="Matrix data stream",
    )
    axis.plot(
        frame["time"], frame["rolling_mean"],
        color="white", linewidth=1.6, label="Rolling mean (20)",
    )
    axis.set_title("Matrix Data Stream Analysis", color="#00ff41")
    axis.set_xlabel("Time", color="#00ff41")
    axis.set_ylabel("Signal", color="#00ff41")
    axis.legend(loc="upper left")
    axis.set_facecolor("#0d0d0d")
    figure.set_facecolor("#0d0d0d")
    axis.tick_params(colors="#00ff41")
    figure.tight_layout()
    figure.savefig(OUTPUT_FILE, dpi=120)
    plt.close(figure)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


def main() -> None:
    """Check dependencies, then analyse or guide the user to install."""
    print("LOADING STATUS: Loading programs...")
    print()
    ready = check_dependencies()
    if not ready:
        print_install_help()
        compare_package_managers()
        sys.exit(1)
    run_analysis()
    compare_package_managers()


if __name__ == "__main__":
    main()
