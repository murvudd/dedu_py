import asyncio
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tqdm.asyncio import tqdm  # Używamy wersji dedykowanej dla asyncio


def hash_file(file_path: Path, chunk_size: int = 65536) -> str:
    if not isinstance(file_path, Path):
        raise TypeError(f"file_path: {file_path} must be a Path object")
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path} is not a file")

    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # Czytamy plik kawałek po kawałku
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


async def hash_map(file_list: list[Path], max_concurrent: int = 20) -> dict[Path, str]:
    loop = asyncio.get_running_loop()
    sem = asyncio.Semaphore(max_concurrent)
    with ThreadPoolExecutor() as executor:

        async def bounded_hash(path: Path):
            async with sem:
                # Wykonujemy ciężką pracę w wątku (bez GIL w 3.14t!)
                h = await loop.run_in_executor(executor, hash_file, path)
                return path, h

        # Tworzymy listę zadań
        tasks = [bounded_hash(p) for p in file_list]

        # tqdm.asyncio.gather automatycznie obsłuży pasek postępu
        # 'desc' to ten krótki, konkretny opis, o który dbaliśmy
        mapped_results = await tqdm.gather(
            *tasks,
            desc="🍑 dedu.py | Hashing files",
            unit="file",
            colour="green",
            mininterval=0.5,
        )

    return dict(mapped_results)
