import json
import logging
import os
import tempfile
from collections import defaultdict
from pathlib import Path

from .hash import hash_map


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


def find_duplicates(hashes: dict[Path, str]) -> dict[str, list[str]]:
    """
    Grupuje ścieżki plików według ich hashy MD5.
    Zwraca tylko te, które występują więcej niż raz.
    """
    grouped = defaultdict(list)

    # Grupowanie (odwracamy słownik)
    for path, file_hash in hashes.items():
        grouped[file_hash].append(str(path))

    # Filtrowanie - zostawiamy tylko prawdziwe duplikaty
    duplicates = {f_hash: paths for f_hash, paths in grouped.items() if len(paths) > 1}

    return duplicates


def save_report(duplicates: dict[str, list[str]], report_path: Path = Path("duplicates.json")):
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(duplicates, f, indent=4, ensure_ascii=True)
    return report_path


async def main(
    source_dir: Path = None,
    dry_run: bool = False,
    max_concurrent: int = 20,
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

    temp_dir = tempfile.mkdtemp()
    logging.debug(f"temp_dir: {temp_dir}")
    print("🍑 dedu.py: Scanning directory ...")

    all_files_in_directory: list[Path] = recursive_dir_list(source_dir)

    print(f"📂  found {len(all_files_in_directory)} files.")
    print("🍑 dedu.py: Scanning for duplicates...")
    dict_map_hash = await hash_map(all_files_in_directory, max_concurrent=max_concurrent)
    print("#️⃣ hasing files complete.")
    duplicates = find_duplicates(dict_map_hash)

    logging.debug(f"duplicates: {duplicates}")
    print(f" {len(duplicates)} duplicates found.")
    save_report(duplicates)
    #
