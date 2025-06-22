"""Ponto de entrada da aplicação."""

import logging

from .interfaces.views.gui import criar_interface
from .telemetry import init as init_telemetry


def main() -> None:
    """Configure logging and start the interface."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )
    init_telemetry()
    criar_interface()


if __name__ == "__main__":
    main()
