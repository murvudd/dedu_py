#! ./.venv/bin/python
import asyncio
import logging
import os
from pathlib import Path
from sys import argv

from src.dedupy.__init__ import main

DEBUG = os.environ.get("DEBUG", "")
DEBUG = DEBUG.lower() == "true"

log_lvl = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(level=log_lvl, format="[%(levelname)s]::%(asctime)s::  %(message)s")
logging.getLogger(__name__).addHandler(logging.NullHandler())

if DEBUG:
    logging.debug(f"🧑‍💻 running in DEBUG mode == {DEBUG}")

# TODO: use click to handle cli args.
if __name__ == "__main__":
    argv = argv[1:]

    asyncio.run(main(source_dir=Path(argv[0]), dry_run=True))
