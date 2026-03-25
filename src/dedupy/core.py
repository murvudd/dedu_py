import logging
import os
import tempfile

from pathlib import Path

import asyncio

DEBUG = os.environ.get("DEBUG", "")
DEBUG = DEBUG.lower() == "true"

log_lvl = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(level=log_lvl, format="[%(levelname)s]::%(asctime)s::\t%(message)s")
logging.getLogger(__name__).addHandler(logging.NullHandler())

async def dir_list(source:Path)->list[Path]:
    assert source.is_dir(), ValueError(f"{source} is not a directory")
    _list = os.listdir(source)
    res = [Path(x).absolute() for x in _list]
    return res

async def main(
    source_dir: Path = None,
    dry_run: bool = False,
):
    """

    :param source_dir:
    :param dry_run:
    :return:
    """



    if source_dir is None:
        source_dir = Path(".").absolute()
    print(f"👀 in {source_dir}")

    if dry_run:
        print("🚫 💦 runnig dry; (NO FILE CHANGES)")

    if DEBUG:
        logging.getLogger("dedup").setLevel(logging.DEBUG)
        logging.debug(f"🧑‍💻running in DEBUG mode == {DEBUG}")

    temp_dir = tempfile.mkdtemp()
    logging.debug(f"temp_dir: {temp_dir}")

    dir_list = os.listdir(source_dir)
    logging.debug(f"dir_list: {dir_list}")

    print("🍑 dedu.py: Scanning for duplicates...")
