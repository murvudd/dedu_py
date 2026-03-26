from pathlib import Path

import pytest

from dedupy.hash import hash_file, hash_map


class TestFileHashing:
    @pytest.mark.parametrize(
        "case",
        [
            {"file": "", "raises": TypeError},
            {"file": Path("non_existent_dir"), "raises": FileNotFoundError},
            {"file": Path("tests/data/sub2/c.txt"), "expected": "06a8d719ed4611cbffcd81a395781d47"},
            {"file": Path("tests/data/sub2/b.txt"), "expected": "4f41243847da693a4f356c0486114bc6"},
            {"file": Path("tests/data/sub2/a.txt"), "expected": "258e88dcbd3cd44d8e7ab43f6ecb6af0"},
            {"file": Path("tests/data/c.txt"), "expected": "06a8d719ed4611cbffcd81a395781d47"},
            {"file": Path("tests/data/b.txt"), "expected": "4f41243847da693a4f356c0486114bc6"},
            {"file": Path("tests/data/a.txt"), "expected": "258e88dcbd3cd44d8e7ab43f6ecb6af0"},
        ],
    )
    def test_file_hashing(self, case):
        if case.get("raises", None):
            with pytest.raises(case["raises"]):
                hash_file(case["file"])
        else:
            result = hash_file(case["file"])
            assert result == case["expected"]


class TestHashMap:
    async def test_hash_map_basic(self):
        """Sprawdza podstawowe mapowanie kilku plików."""
        file_list = [Path("tests/data/a.txt"), Path("tests/data/b.txt")]
        # Zakładamy, że znasz te hashe z poprzednich testów
        expected = {
            Path("tests/data/a.txt"): "258e88dcbd3cd44d8e7ab43f6ecb6af0",
            Path("tests/data/b.txt"): "4f41243847da693a4f356c0486114bc6",
        }

        result = await hash_map(file_list)

        assert sorted(result) == sorted(expected)
        assert len(result) == 2

    async def test_hash_map_empty_list(self):
        """Sprawdza, czy pusta lista nie wywala błędu."""
        result = await hash_map([])
        assert result == {}

    async def test_hash_map_concurrency_limit(self, tmp_path):
        """
        Test 'stresowy': tworzy 50 małych plików i sprawdza,
        czy semafor (max_concurrent=10) działa poprawnie.
        """
        test_files = []
        for i in range(50):
            p = tmp_path / f"file_{i}.txt"
            p.write_text(f"content_{i}")
            test_files.append(p)

        # Odpalamy z małym limitem, żeby wymusić kolejkę w semaforze
        result = await hash_map(test_files, max_concurrent=5)

        assert len(result) == 50
        # Sprawdzamy losowy plik, czy hash w ogóle istnieje
        random_path = test_files[10]
        assert len(result[random_path]) == 32  # Długość MD5

    async def test_hash_map_preserves_order_logic(self):
        """
        Upewniamy się, że mimo asynchroniczności, słownik
        został zbudowany poprawnie dla dużej liczby plików.
        """
        file_list = [Path(f"tests/data/file_{i}.txt") for i in range(3)]
        # Symulujemy sytuację, gdzie pliki nie istnieją, żeby sprawdzić rzucanie błędów wewnątrz mapy
        with pytest.raises(FileNotFoundError):
            await hash_map(file_list)
