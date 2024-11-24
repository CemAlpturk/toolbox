from typing import Any
import pathlib
import pytest

from toolbox.parsing import (
    read_lines,
    read_ints,
    parse_grid,
    # parse_blocks,
    # parse_csv,
    # parse_numbers_from_text,
    parse_key_value_pairs,
)


def test_read_lines(tmp_path: pathlib.PosixPath) -> None:
    """Test reading lines from a file with default stripping."""
    test_file = tmp_path / "test_lines.txt"
    print(type(tmp_path))
    test_file.write_text("Line 1\nLine 2\nLine 3\n")

    expected_lines = ["Line 1", "Line 2", "Line 3"]
    lines = read_lines(str(test_file))
    assert lines == expected_lines


def test_read_lines_no_strip(tmp_path: pathlib.PosixPath) -> None:
    """Test reading lines from a file without stripping newline characters."""
    test_file = tmp_path / "test_lines_no_strip.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\n")

    expected_lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
    lines = read_lines(str(test_file), strip=False)
    assert lines == expected_lines


def test_read_ints(tmp_path: pathlib.PosixPath) -> None:
    """Test reading integers from a file."""
    test_file = tmp_path / "test_ints.txt"
    test_file.write_text("1\n2\n3\n")

    expected_ints = [1, 2, 3]
    ints = read_ints(str(test_file))
    assert ints == expected_ints


def test_read_ints_invalid_data(tmp_path: pathlib.PosixPath) -> None:
    """Test read_ints with invalid data."""
    test_file = tmp_path / "test_ints_invalid.txt"
    test_file.write_text("1\n2\nthree\n")

    with pytest.raises(ValueError):
        read_ints(str(test_file))


def test_parse_grid_with_delimiter(tmp_path):
    """Test parsing a grid with a space delimiter."""
    test_file = tmp_path / "test_grid.txt"
    test_file.write_text("1 2 3\n4 5 6\n7 8 9\n")

    expected_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = parse_grid(str(test_file), int, delimiter=" ")
    assert grid == expected_grid


def test_parse_grid_no_delimiter(tmp_path):
    """Test parsing a grid without a delimiter (character by character)."""
    test_file = tmp_path / "test_grid_no_delim.txt"
    test_file.write_text("ABC\nDEF\nGHI\n")

    expected_grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    grid = parse_grid(str(test_file), lambda x: x)
    assert grid == expected_grid


def test_parse_grid_invalid_data(tmp_path):
    """Test parse_grid with invalid casting data."""
    test_file = tmp_path / "test_grid_invalid.txt"
    test_file.write_text("1 2 3\n4 five 6\n7 8 9\n")

    with pytest.raises(ValueError):
        parse_grid(str(test_file), int, delimiter=" ")


def test_parse_key_value_pairs_default(tmp_path):
    """Test parsing key-value pairs with default delimiters."""
    test_file = tmp_path / "test_key_value.txt"
    test_file.write_text("key1:value1\nkey2:value2\nkey3:value3\nkey4:value4\n")

    expected_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    data = parse_key_value_pairs(str(test_file))
    assert data == expected_data


def test_parse_key_value_pairs_custom_delimiters(tmp_path):
    """Test parsing key-value pairs with custom delimiters."""
    test_file = tmp_path / "test_key_value_custom.txt"
    test_file.write_text("key1=value1||key2=value2||key3=value3||key4=value4")

    expected_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    data = parse_key_value_pairs(
        str(test_file),
        item_delimiter="||",
        key_value_delimiter="=",
        key_cast=str,
        value_cast=str,
    )
    assert data == expected_data


def test_parse_key_value_pairs_invalid_data(tmp_path):
    """Test parse_key_value_pairs with invalid data."""
    test_file = tmp_path / "test_key_value_invalid.txt"
    test_file.write_text("key1:value1\nkey2\n")

    with pytest.raises(ValueError):
        parse_key_value_pairs(str(test_file))
