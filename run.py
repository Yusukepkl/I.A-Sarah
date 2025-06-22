import sys
from pathlib import Path

# Add src to sys.path to allow running without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ia_sarah.core.main import main

if __name__ == "__main__":
    main()
