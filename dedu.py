#! ./.venv/bin/python
import asyncio
from pathlib import Path
from sys import argv

from src.dedupy.__init__ import main

# TODO: use click to handle cli args.
if __name__ == "__main__":
    argv = argv[1:]

    asyncio.run(
        main(source_dir=Path(argv[0]).absolute(), dry_run=True)
    )
