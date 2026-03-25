from pathlib import Path

import pytest

from dedupy.core import dir_list, hash_file, recursive_dir_list


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


class TestFileHashing:
    @pytest.mark.parametrize(
        "case",
        [
            {"file": "", "raises": FileNotFoundError},
            {"file": Path("non_existent_dir"), "raises": FileNotFoundError},
            {"file": Path("tests/data/sub2/c.txt"), "expected": "06a8d719ed4611cbffcd81a395781d47"},
            {"file": Path("tests/data/sub2/b.txt"), "expected": "4f41243847da693a4f356c0486114bc6"},
            {"file": Path("tests/data/sub2/a.txt"), "expected": "258e88dcbd3cd44d8e7ab43f6ecb6af0"},
            {"file": Path("tests/data/c.txt"), "expected": "06a8d719ed4611cbffcd81a395781d47"},
            {"file": Path("tests/data/b.txt"), "expected": "4f41243847da693a4f356c0486114bc6"},
            {"file": Path("tests/data/a.txt"), "expected": "258e88dcbd3cd44d8e7ab43f6ecb6af0"},
        ],
    )
    async def test_file_hashing(self, case):
        if case.get("raises", None):
            with pytest.raises(case["raises"]):
                await hash_file(case["file"])
        else:
            result = await hash_file(case["file"])
            assert result == case["expected"]
