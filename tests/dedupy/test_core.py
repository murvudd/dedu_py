import json
from pathlib import Path

import pytest

from dedupy.core import find_duplicates, recursive_dir_list, save_report


class TestDirectoryListing:
    @pytest.mark.parametrize(
        "case",
        [
            {"dir": "", "raises": AttributeError},  # dir is not Path
            {"dir": Path("non_existent_dir"), "raises": ValueError},
            {"dir": Path("tests/data/sub1"), "expected": []},  # empty dir
            {
                "dir": Path("tests/data/sub2"),
                "expected": [
                    Path("tests/data/sub2/c.txt"),
                    Path("tests/data/sub2/b.txt"),
                    Path("tests/data/sub2/a.txt"),
                ],
            },
            {
                "dir": Path("tests/data"),
                "expected": [
                    Path("tests/data/c.txt"),
                    Path("tests/data/b.txt"),
                    Path("tests/data/a.txt"),
                    Path("tests/data/sub2/c.txt"),
                    Path("tests/data/sub2/b.txt"),
                    Path("tests/data/sub2/a.txt"),
                ],
            },
        ],
    )
    def test_recuresive_dir_list(self, case):
        if case.get("raises", None):
            with pytest.raises(case["raises"]):
                recursive_dir_list(case["dir"])
        else:
            result = recursive_dir_list(case["dir"])
            assert sorted(result) == sorted(case["expected"])


#


class TestDuplicateLogic:
    def test_find_duplicates_logic(self):
        # Mockujemy dane wejściowe
        mock_hashes = {
            Path("a.txt"): "hash1",
            Path("b.txt"): "hash1",  # Duplikat
            Path("c.txt"): "hash2",  # Unikalny
            Path("d.txt"): "hash3",
            Path("e.txt"): "hash3",  # Kolejny duplikat
        }

        result = find_duplicates(mock_hashes)

        assert len(result) == 2  # Tylko hash1 i hash3 powinny zostać
        assert "hash1" in result
        assert len(result["hash1"]) == 2
        assert "hash2" not in result  # Unikalne pliki znikają

    def test_save_report(self, tmp_path):
        report_file = tmp_path / "test_report.json"
        data = {"some_hash": ["file1.txt", "file2.txt"]}

        path = save_report(data, report_file)

        assert path.exists()
        with open(path) as f:
            loaded = json.load(f)
            assert loaded == data
