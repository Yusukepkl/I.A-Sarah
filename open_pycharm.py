#!/usr/bin/env python3
"""Abre o projeto I.A-Sarah no PyCharm."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Tenta executar o comando ``pycharm`` apontando para a raiz."""
    repo_root = Path(__file__).resolve().parent
    try:
        subprocess.run(["pycharm", str(repo_root)], check=True)
    except FileNotFoundError:
        sys.exit("PyCharm não encontrado. Adicione 'pycharm' ao PATH.")


if __name__ == "__main__":
    main()
