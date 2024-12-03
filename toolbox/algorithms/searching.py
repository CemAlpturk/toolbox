from typing import Callable, Optional, TypeVar, Any, Protocol


class Proto(Protocol):
    def __lt__(self, other: "Proto") -> bool: ...
    def __le__(self, other: "Proto") -> bool: ...
    def __gt__(self, other: "Proto") -> bool: ...
    def __ge__(self, other: "Proto") -> bool: ...


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
        >>> print(index) #  Output: 2
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


def lower_bound(
    arr: list[T],
    target: T,
    key: Callable[[T], K] = lambda x: x,
) -> int:
    """
    Finds the first index where `arr[index] >= target`.

    Args:
        arr (list[T]): The sorted array to search.
        target (T): The target value.
        key (Callable[[T], K], optional): A function to extract a comparison key from each element. Defaults to identity function.

    Returns:
        int: The index of the lower bound.

    Example:
        >>> arr = [1, 3, 3, 5, 7]
        >>> index = lower_bound(arr, 3)
        >>> print(index) #  Output: 1
    """
    left, right = 0, len(arr)
    target_key = key(target)

    while left < right:
        mid = (left + right) // 2
        if key(arr[mid]) < target_key:
            left = mid + 1
        else:
            right = mid

    return left


def upper_bound(arr: list[T], target: T, key: Callable[[T], K] = lambda x: x) -> int:
    """
    Finds the first index where `arr[index] > target`.

    Args:
        arr (list[T]): The sorted array to search.
        target (T): The target value.
        key (Callable[[T], K], optional): A function to extract a comparison key from each element. Defaults to identity function.

    Returns:
        int: The index of the upper bound.

    Example:
        >>> arr = [1, 3, 3, 5, 7]
        >>> index = upper_bound(arr, 3)
        >>> print(index)  # Output: 3
    """
    left, right = 0, len(arr)
    target_key = key(target)

    while left < right:
        mid = (left + right) // 2
        if key(arr[mid]) <= target_key:
            left = mid + 1
        else:
            right = mid

    return left
