from pathlib import Path

import pytest

from dedupy.core import dir_list, recursive_dir_list


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
                    Path("tests/data/sub1"),
                    Path("tests/data/c.txt"),
                    Path("tests/data/b.txt"),
                    Path("tests/data/a.txt"),
                    Path("tests/data/sub2"),
                ],
            },
        ],
    )
    def test_dir_list(self, case):
        if case.get("raises", None):
            with pytest.raises(case["raises"]):
                dir_list(case["dir"])
        else:
            result = dir_list(case["dir"])
            assert sorted(result) == sorted(case["expected"])

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
