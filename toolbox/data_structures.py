from typing import (
    Any,
    Generic,
    TypeVar,
    Callable,
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


class SegmentTree(Generic[T]):
    """
    Segment Tree implementation for range queries and updates.
    """

    def __init__(
        self,
        data: list[T],
        func: Callable[[T, T], T],
        default: T,
    ) -> None:
        """
        Initializes the Segment Tree.

        Args:
            data (list[T]): The initial array.
            func (Callable[[T, T], T]): The function to combine elements (e.g., sum, min, max).
            default (T): The default value for non-initialized nodes.
        """
        self.n = len(data)
        self.func = func
        self.default = default
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [default] * (2 * self.size)
        self.build(data)

    def build(self, data: list[T]) -> None:
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index: int, value: T) -> None:
        """
        Updates the value at the specified index.

        Args:
            index (int): The index to update.
            value (T): The new value.
        """
        index += self.size
        self.tree[index] = value
        while index > 1:
            index >>= 1
            self.tree[index] = self.func(self.tree[2 * index], self.tree[2 * index + 1])

    def query(self, left: int, right: int) -> T:
        """
        Queries the function over the range [left, right).

        Args:
            left (int): The starting index (inclusive).
            right (int): The ending index (exclusive).

        Returns:
            T: The result of the function over the range.
        """
        result = self.default
        left += self.size
        right += self.size

        while left < right:
            if left % 2:
                result = self.func(result, self.tree[left])
                left += 1
            if right % 2:
                right -= 1
                result = self.func(result, self.tree[right])
            left >>= 1
            right >>= 1

        return result


class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) implementation for prefix ops.
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree: list[int] = [0] * (size + 1)

    def update(self, index: int, value: int) -> None:
        """
        Adds `value` to the element at `index`.

        Args:
            index (int): The index to update (0-based).
            value (int): The value to add.
        """
        index += 1  # Convert to 1-based indexing
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def query(self, index: int) -> int:
        """
        Computes the prefix sum up to and including `index`.

        Args:
            index (int): The index to query (0-based).

        Returns:
            int: The prefix op.
        """
        index += 1  # Convert to 1-based indexing
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result

    def range_query(self, left: int, right: int) -> int:
        """
        Computes the range sum between `left` and `right` inclusive.

        Args:
            left (int): The starting index (0-based).
            right (int): The ending index (1-based).

        Returns:
            int: The op over the range.
        """
        return self.query(right) - self.query(left - 1)


class ListNode:
    """
    A node in a singly linked list.
    """

    def __init__(self, value: Any):
        self.value = value
        self.next: ListNode | None = None


class LinkedList:
    """
    A simple linked list.
    """

    def __init__(self):
        self.head: ListNode | None = None

    def insert(self, value: Any) -> None:
        """
        Inserts a new node with the given value at the beginning.

        Args:
            value (Any): The value to insert.
        """
        new_node = ListNode(value)
        new_node.next = self.head
        self.head = new_node

    def delete(self, value: Any) -> bool:
        """
        Deletes the first node with the specified value.

        Args:
            value (Any): The value to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        prev = None
        curr = self.head
        while curr:
            if curr.value == value:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev = curr
            curr = curr.next
        return False

    def find(self, value: Any) -> ListNode | None:
        """
        Finds the first node wit the specified value.

        Args:
            value (Any): The value to find.

        Returns:
            ListNode | None: The node if found, None otherwise.
        """
        curr = self.head
        while curr:
            if curr.value == value:
                return curr
            curr = curr.next
        return None

    def to_list(self) -> list[Any]:
        """
        Converts the linked list to a Python list.

        Returns:
            list[Any]: the list of node values.
        """
        result = []
        curr = self.head
        while curr:
            result.append(curr.value)
            curr = curr.next
        return result
