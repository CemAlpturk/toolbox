from typing import (
    Callable,
    TypeVar,
    Optional,
    Any,
    Union,
    Iterable,
)
import re

T = TypeVar("T")


def read_lines(
    filename: str,
    strip: bool = True,
) -> list[str]:

    lines: list[str] = []
    with open(filename, "r") as file:
        for line in file:
            if strip:
                line = line.strip("\n")
            lines.append(line)
    return lines


def read_ints(filename: str) -> list[int]:

    lines = read_lines(filename, strip=True)
    ints: list[int] = []
    for line_number, line in enumerate(lines, 1):
        try:
            number = int(line)
            ints.append(number)
        except ValueError as e:
            print(f"Error parsing integer on line {line_number}: {e}")
            raise

    return ints


def parse_grid(
    filename: str,
    cast: Callable[[str], T],
    delimiter: str | None = None,
) -> list[list[T]]:

    grid: list[list[T]] = []
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
            line = line.rstrip("\n")
            if delimiter is not None:
                elements = line.split(delimiter)
            else:
                elements = list(line)
            try:
                row = [cast(element) for element in elements]
                grid.append(row)
            except ValueError as e:
                print(f"Error casting element on line {line_number}: {e}")
                raise

    return grid


def parse_key_value_pairs(
    filename: str,
    item_delimiter: str = "\n",
    key_value_delimiter: str = ":",
    key_cast: Callable[[str], Any] = lambda x: x,
    value_cast: Callable[[str], Any] = lambda x: x,
) -> dict:

    with open(filename, "r") as file:
        content = file.read()

    items = content.strip().split(item_delimiter)
    data: dict = {}

    for item_number, item in enumerate(items, 1):
        pair = item.strip()
        if key_value_delimiter in pair:
            key_str, value_str = pair.split(key_value_delimiter, 1)
            try:
                key = key_cast(key_str)
                value = value_cast(value_str)
                data[key] = value
            except ValueError as e:
                print(f"Error casting key or value in item {item_number}: {e}")
                raise

        else:
            print(f"Invalid key-value pair in item {item_number}: '{pair}'")
            raise ValueError(f"Invalid key-value pair: '{pair}'")

    return data
