from typing import Callable, Optional, TypeVar, Any, Protocol


class Proto(Protocol):
    def __lt__(self, other: "Proto") -> bool: ...
    def __gt__(self, other: "Proto") -> bool: ...


T = TypeVar("T", bound=Proto)
K = TypeVar("K", bound=Proto)


def binary_search(
    arr: list[T],
    target: T,
    key: Callable[[T], K] = lambda x: x,
) -> int:
    """
    Performs binary search on a sorted array.

    Args:
        arr (list[T]): The sorted array to search.
        target (T): The target value to find.
        key (Callable[[T], K], optional): A function to extract a comparison key from each element. Defaults to identity function.

    Returns:
        int: The index of the target in the array if found, else -1.

    Example:
        >>> arr = [1, 3, 5, 7, 9]
        >>> index = binary_search(arr, 5)
        >>> print(index) # Output: 2
    """

    left, right = 0, len(arr) - 1
    target_key = key(target)

    while left <= right:
        mid = (left + right) // 2
        mid_key = key(arr[mid])

        if mid_key == target_key:
            return mid
        elif mid_key < target_key:
            left = mid + 1
        else:
            right = mid - 1

    return -1
