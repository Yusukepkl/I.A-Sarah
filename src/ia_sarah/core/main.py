"""Ponto de entrada da aplicação."""

import logging

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[2]))

from ia_sarah.core.telemetry import init as init_telemetry
from ia_sarah.core.interfaces.views.gui import criar_interface


def main() -> None:
    """Configure logging and start the interface."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    init_telemetry()
    criar_interface()


if __name__ == "__main__":
    main()
