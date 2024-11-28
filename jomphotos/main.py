import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication

from jomphotos import app


def main():
    # Argument parsing setup
    parser = argparse.ArgumentParser(description="Image Sorting Application")
    parser.add_argument("--dir", type=str, help="Directory to load images from.")
    args = parser.parse_args()

    initial_directory = args.dir if args.dir and os.path.isdir(args.dir) else None

    app_instance = QApplication(sys.argv)
    ui = app(initial_directory)  # Pass the directory
    ui.show()  # Show the main window app instance creation
    sys.exit(app_instance.exec_())


if __name__ == "__main__":
    main()
