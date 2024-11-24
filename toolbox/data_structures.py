from typing import Any


class UnionFind:
    """
    Union-Find data structure (Disjoint Set Union - DSU)
    """

    def __init__(self) -> None:
        self.parent: dict[Any, Any] = {}
        self.rank: dict[Any, int] = {}

    def find(self, item: Any) -> Any:
        """
        Finds the representative (root) of the set that 'item' belongs to.
        Uses path compression for efficiency.

        Args:
            item (Any): The item to find.

        Returns:
            Any: The representative of the set.
        """

        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0
            return item

        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])

        return self.parent[item]

    def union(self, x: Any, y: Any) -> None:
        """
        Unites the sets that contain 'x' and 'y'.

        Args:
            x (Any): An item in the first set.
            y (Any): An item in the second set.
        """

        xroot = self.find(x)
        yroot = self.find(y)

        if xroot == yroot:
            return

        # Union by rank to keep tree shallow
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        else:
            self.parent[yroot] = xroot
            if self.rank[xroot] == self.rank[yroot]:
                self.rank[xroot] += 1
