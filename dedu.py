#!/usr/bin/env python
import asyncio
import logging
import os
from pathlib import Path

import click

from dedupy.__init__ import main as dedupy_main

# --- Konfiguracja Logowania ---
DEBUG = os.environ.get("DEBUG", "").lower() == "true"
log_lvl = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(level=log_lvl, format="[%(levelname)s]::%(asctime)s::  %(message)s")

logger = logging.getLogger(__name__)


# --- CLI z Click ---
@click.command()
@click.argument("source_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--dry-run", is_flag=True, default=True,show_default=True, help="Find duplicates, without removing anything.")
@click.option('--report', default="duplicates.json",type=Path,show_default=True, help="Path to result file")
@click.option(
    '--max-concurrent',
    type=int,
    default=20,
    show_default=True,
    help="Maximum number of concurrent dedu.py jobs."
)
def cli(source_dir, dry_run, report ,max_concurrent):
    """🍑 dedu-py: Ultra-fast and ridiculously simple file deduplication."""

    if DEBUG:
        logger.debug(f"🧑‍💻 running in DEBUG mode == {DEBUG}")

    asyncio.run(dedupy_main(source_dir=source_dir, dry_run=dry_run, report_path=report, max_concurrent=max_concurrent))


if __name__ == "__main__":
    cli()
