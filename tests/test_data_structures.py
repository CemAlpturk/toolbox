import pytest

from toolbox.data_structures import (
    UnionFind,
    PriorityQueue,
    Trie,
    SegmentTree,
    FenwickTree,
    LinkedList,
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


def test_trie_operations() -> None:
    """Test Trie insert, search, and starts_with."""
    trie = Trie()
    words = ["apple", "app", "application"]

    for word in words:
        trie.insert(word)

    # Test search
    assert trie.search("app")
    assert trie.search("apple")
    assert trie.search("application")
    assert not trie.search("apples")

    # Test starts_with
    assert trie.starts_with("app")
    assert trie.starts_with("appl")
    assert not trie.starts_with("banana")


def test_segment_tree_sum():
    """Test SegmentTree for range sum queries and updates."""
    data = [1, 3, 5, 7, 9, 11]
    seg_tree = SegmentTree(data, func=lambda x, y: x + y, default=0)

    # Query sum from index 1 to 5
    assert seg_tree.query(1, 5) == 24

    # Update index 3 to value 10
    seg_tree.update(3, 10)

    # Query again after the update
    assert seg_tree.query(1, 5) == 27


def test_segment_tree_min():
    """Test SegmentTree for range minimum queries."""
    data = [5, 2, 6, 3, 7, 1]
    seg_tree = SegmentTree(data, func=min, default=float("inf"))  # type: ignore

    # Query min from index 1 to 4
    assert seg_tree.query(1, 5) == 2

    # Update index 2 to value 0
    seg_tree.update(2, 0)

    # Query again after the update
    assert seg_tree.query(1, 5) == 0


def test_fenwick_tree() -> None:
    """Test FenwickTree for prefix sums and range queries."""
    data = [1, 2, 3, 4, 5]
    fenwick = FenwickTree(len(data))

    # Buld the tree
    for idx, val in enumerate(data):
        fenwick.update(idx, val)

    # Query prefix sum up to index 3
    assert fenwick.query(3) == 10

    # Range sum from index 1 to 3
    assert fenwick.range_query(1, 3) == 9

    # Update index 2 by adding 5
    fenwick.update(2, 5)

    # Query again after the update
    assert fenwick.query(3) == 15


def test_linked_list_operations() -> None:
    """Test LinkedList insert, delete, find, and to_list."""
    ll = LinkedList()
    ll.insert(3)
    ll.insert(2)
    ll.insert(1)

    # The list should be [1, 2, 3]
    assert ll.to_list() == [1, 2, 3]

    # Delete a middle element
    assert ll.delete(2)
    assert ll.to_list() == [1, 3]

    # Delete a non-existent element
    assert not ll.delete(4)

    # Find an element
    node = ll.find(3)
    assert node is not None and node.value == 3

    # Find a non-existent element
    node = ll.find(4)
    assert node is None
