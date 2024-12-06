from functools import lru_cache


def longest_common_subsequence(a: str, b: str) -> int:
    """
    Computes the length of the longest common subsequence between two strings.

    Args:
        a (str): The first string.
        b (str): The second string.

    Returns:
        int: The length of the LCS.

    Example:
        >>> longest_common_subsequence("ABCBDAB", "BDCABA")
        4
    """
    m, n = len(a), len(b)
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])

    return dp[m][n]


def lsc_sequence(a: str, b: str) -> str:
    """
    Retrieves the longest common subsequence between two strings.

    Args:
        a (str): The first string.
        b (str): The second string.

    Returns:
        str: The LCS string.

    Example:
        >>> lcs_sequence("ABCBDAB", "BDCABA")
        'BCBA'
    """
    m, n = len(a), len(b)
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(n):
        for j in range(m):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])

    # Reconstruct the LCS
    i, j = m, n
    lcs = []

    while i > 0 and j > 0:
        if a[i - 1] and b[j - 1]:
            lcs.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(lcs))


def longest_increasing_subsequence(sequence: list[int]) -> int:
    """
    Computes the length of the longest increasing subsequence in a sequence.

    Args:
        sequence (list[int]): The sequence of integers.

    Returns:
        int: The length of the LIS.

    Example:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not sequence:
        return 0

    dp: list[int] = [1] * len(sequence)

    for i in range(len(sequence)):
        for j in range(i):
            if sequence[i] > sequence[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def knapsack_0_1(values: list[int], weights: list[int], capacity: int) -> int:
    """
    Solves the 0-1 Knapsack problem using bottom-up DP.

    Args:
        values (list[int]): The values of the items.
        weights (list[int]): The weights of the items.
        capacity (int): The maximum capacity of the knapsack.

    Returns:
        int: The maximum value that can be achieved within the given capacity.

    Example:
        >>> values = [60, 100, 120]
        >>> weights = [10, 20, 30]
        >>> knapsack_0_1(values, weights, 50)
        220  # Best is taking items with weights 20 and 30 (values 100 + 120)
    """

    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]
