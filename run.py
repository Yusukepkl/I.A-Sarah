import sys
from pathlib import Path


def main() -> None:
    """Entry point for running the application without installation."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
    import ia_sarah.core.main

    ia_sarah.core.main.main()


if __name__ == "__main__":
    main()
