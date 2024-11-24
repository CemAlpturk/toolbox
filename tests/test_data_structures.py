import pytest

from toolbox.data_structures import (
    UnionFind,
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
