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


def ternary_search(
    func: Callable[[float], float],
    left: float,
    right: float,
    absolute_precision: float = 1e-7,
) -> float:
    """
    Performs ternary search on a unimodal function to find its minimum value within [left, right].

    Args:
        func (Callable[[float], float]): The unimodal functionto minimuze.
        left (float): The left boundary of the search interval.
        right (float): The right boundary of the search interval.
        absolute_precisiton(float, optional): The precision of the result. Defaults to 1e-7.

    Returns:
        float: the x-coordinate of the minimum value.

    Example:
        >>> def f(x):
        ...     return (x - 2) ** 2
        >>> min_x = ternary_search(f, 0, 5)
        >>> print(f"{min_x:.5f}")  # Output: 2.00000
    """
    while right - left > absolute_precision:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3
        f1 = func(mid1)
        f2 = func(mid2)
        if f1 < f2:
            right = mid2
        else:
            left = mid1

    return (left + right) / 2


def exponential_search(
    arr: list[T], target: T, key: Callable[[T], K] = lambda x: x
) -> int:
    """
    Performs exponential search to find the range where the target may exists, then uses binary search.

    Args:
        arr (list[T]): The sorted array to search.
        target (T): The target value.
        key (Callable[[T], K], optional): A function toe extract a comparison key. Defaults to identity function.

    Returns:
        int: The index of the target if found, else -1.

    Example:
        >>> arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> index = exponential_search(arr, 7)
        >>> print(index)  # Output: 6
    """
    if not arr:
        return -1

    n = len(arr)
    bound = 1
    target_key = key(target)

    while bound < n and key(arr[bound]) < target_key:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)
    return binary_search(arr[left : right + 1], target, key=key) + left
