"""Ponto de entrada da aplicação."""

import logging

from gui import criar_interface


def main() -> None:
    """Configure logging and start the interface."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    criar_interface()

if __name__ == "__main__":
    main()
