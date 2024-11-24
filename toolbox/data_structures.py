from typing import (
    Any,
    Generic,
    TypeVar,
)
import heapq

T = TypeVar("T")


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


class PriorityQueue(Generic[T]):
    """
    A simple Priority Queue implementation using a heap.
    """

    def __init__(
        self,
        items: list[T] | None = None,
        key=lambda x: x,
    ) -> None:

        self.key = key
        self._data = []
        if items:
            for item in items:
                self.push(item)

    def push(self, item: T) -> None:
        """
        Pushes an ite onto the priority queue.

        Args:
            item (T): The item  to be added.
        """
        heapq.heappush(self._data, (self.key(item), item))

    def pop(self) -> T:
        """
        Removes and returns the smallest item from the queue.

        Returns:
            T: The smallest item.
        """
        return heapq.heappop(self._data)[1]

    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.

        Returns:
            bool: True if empty, False otherwise.
        """
        return not self._data

    def peek(self) -> T:
        """
        Returns the smallest item without removing it.

        Returns:
            T: The smallest item.
        """
        return self._data[0][1]


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False


class Trie:
    """
    Trie (Prefix Tree) implementation for efficient string searching.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the Trie.

        Args:
            word (str): The word to insert.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Searches for a word in the Trie.

        Args:
            word (str): The word to search.

        Returns:
            bool: True of the word exists, False otherwise.
        """
        node = self._find_node(word)
        return node.is_end_of_word if node else False

    def starts_with(self, prefix: str) -> bool:
        """
        Checks if any word in the Trie starts with the given prefix.

        Args:
            prefix (str): The prefix to check.

        Returns:
            bool: True if any word starts with the prefix, False otherwise.
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode | None:
        """
        helper function to traverse the Trie up to the end of the prefix.

        Args:
            prefix (str): The prefix to traverse.

        Returns:
            TrieNode | None: The node at the end of the prefix, or None if not found.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
