"""Build executable using PyInstaller."""
from __future__ import annotations

import argparse
from pathlib import Path
import PyInstaller.__main__


def main() -> None:
    """Run PyInstaller with given arguments."""
    parser = argparse.ArgumentParser(description="Build Gestor executables")
    parser.add_argument("--name", default="gestor-alunos", help="Executable name")
    parser.add_argument(
        "--entry", default=str(Path("src/main.py")), help="Entry point of application"
    )
    args = parser.parse_args()
    PyInstaller.__main__.run([
        args.entry,
        "--onefile",
        "--name",
        args.name,
    ])


if __name__ == "__main__":
    main()
