import hashlib
import logging
import os
import tempfile
from pathlib import Path

DEBUG = os.environ.get("DEBUG", "")
DEBUG = DEBUG.lower() == "true"

log_lvl = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(level=log_lvl, format="[%(levelname)s]::%(asctime)s::\t%(message)s")
logging.getLogger(__name__).addHandler(logging.NullHandler())


def dir_list(source: Path) -> list[Path]:
    if not source.is_dir():
        raise ValueError(f"{source} is not a directory")
    _list = os.listdir(source)
    if len(_list) == 0:
        return []
    res = [source / x for x in _list]
    return res


def recursive_dir_list(source: Path) -> list[Path]:
    """
    :param source: Path of root directory, for deduplication
    :return: list[Path] all and only files in root directory
    """
    if not source.is_dir():
        raise ValueError(f"{source} is not a directory")
    _list = os.listdir(source)
    if len(_list) == 0:
        return []
    res = [source / x for x in _list]
    _files = [x for x in res if x.is_file()]
    _dirs = [x for x in res if x.is_dir()]
    if len(_dirs) > 0:
        for dir in _dirs:
            _files.extend(recursive_dir_list(dir))

    return _files


async def hash_map(file_list: list[Path]) -> dict[Path, str]:
    """

    :param file_list:
    :return: dict[Path, str] key: file path, value: md5 hash
    """
    raise NotImplementedError
    return {}


async def hash_file(file_path: Path) -> str:
    if isinstance(file_path, Path):
        pass
    else:
        file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path} is not a file")

    with open(file_path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        return md5


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

    all_files_in_directory: list[Path] = recursive_dir_list(source_dir)
    await hash_map(all_files_in_directory)

    #
    logging.debug(f"dir_list: {dir_list}")

    print("🍑 dedu.py: Scanning for duplicates...")
