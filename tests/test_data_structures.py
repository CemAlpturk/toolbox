import pytest

from toolbox.data_structures import (
    UnionFind,
    PriorityQueue,
)


def test_union_find() -> None:
    """Test UnionFind operations."""
    uf = UnionFind()
    elements = [1, 2, 3, 4, 5]

    # Initially, each element is its own parent
    for elem in elements:
        assert uf.find(elem) == elem

    # Union some elements
    uf.union(1, 2)
    uf.union(3, 4)

    # Test connectivity
    assert uf.find(1) == uf.find(2)
    assert uf.find(3) == uf.find(4)
    assert uf.find(1) != uf.find(3)

    # Union more elements
    uf.union(2, 3)

    # Now all should be connected
    assert uf.find(1) == uf.find(3)
    assert uf.find(1) == uf.find(4)

    # Check that 5 is still in its own set
    assert uf.find(5) == 5


def test_priority_queue_min_heap() -> None:
    """Test PriorityQueue as a min-heap."""
    pq = PriorityQueue()
    pq.push(5)
    pq.push(1)
    pq.push(3)

    expected_order = [1, 3, 5]
    result = []

    while not pq.is_empty():
        result.append(pq.pop())

    assert result == expected_order


def test_priority_queue_max_heap() -> None:
    """Test PriorityQueue as a max-heap using custom key."""
    pq = PriorityQueue(key=lambda x: -x)
    pq.push(5)
    pq.push(1)
    pq.push(3)

    expected_order = [5, 3, 1]
    result = []

    while not pq.is_empty():
        result.append(pq.pop())

    assert result == expected_order
