#!/usr/bin/env python3
"""Abre o projeto I.A-Sarah no Visual Studio Code."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Tenta executar o comando ``code`` apontando para a raiz."""
    repo_root = Path(__file__).resolve().parent
    try:
        subprocess.run(["code", str(repo_root)], check=True)
    except FileNotFoundError:
        sys.exit("VS Code não encontrado. Adicione 'code' ao PATH.")


if __name__ == "__main__":
    main()
