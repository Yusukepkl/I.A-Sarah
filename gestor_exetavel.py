#!/usr/bin/env python3
"""Entrada simplificada para o Gestor de Alunos."""

from __future__ import annotations

import sys
from pathlib import Path

# Add ``src`` to ``sys.path`` when running from a cloned repository.
repo_root = Path(__file__).resolve().parent
src_path = repo_root / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from ia_sarah.core.main import main

if __name__ == "__main__":
    main()
