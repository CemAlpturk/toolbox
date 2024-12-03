from typing import Any, Optional


class TreeNode:
    """
    A node in a binary tree.
    """

    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def in_order_traversal(root: Optional[TreeNode]) -> list[Any]:
    """
    Performs in-order traversal of a binary tree.

    Args:
        root (Optional[TreeNode]): The root node of the tree.

    Returns:
        list[Any]: A list of node values in-order sequence.
    """
    result: list[Any] = []

    def traverse(node: Optional[TreeNode]) -> None:
        if node:
            traverse(node.left)
            result.append(node.value)
            traverse(node.right)

    traverse(root)
    return result


def pre_order_traversal(root: Optional[TreeNode]) -> list[Any]:
    """
    Performs pre-order traversal of a binary tree.

    Args:
        root (Optional[TreeNode]): The root node of the tree.

    Returns:
        list[Any]: A list of node values in pre-order sequence.
    """
    result: list[Any] = []

    def traverse(node: Optional[TreeNode]) -> None:
        if node:
            result.append(node.value)
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return result


def post_order_traversal(root: Optional[TreeNode]) -> list[Any]:
    """
    Performs post-order traversal if a binary tree.

    Args:
        root (Optional[TreeNode]): The root of the tree.

    Returns:
        list[Any]: A list of node values in post-order sequence.
    """
    result: list[Any] = []

    def traverse(node: Optional[TreeNode]) -> None:
        if node:
            traverse(node.left)
            traverse(node.right)
            result.append(node.value)

    traverse(root)
    return result


def bst_insert(root: Optional[TreeNode], value: Any) -> TreeNode:
    """
    Inserts a value into the Binary Search Tree (BST).

    Args:
        root (Optional[TreeNode]): The root node of the BST.
        value (Any): The value to insert.

    Returns:
        TreeNode: The root node of the BST after insertion.
    """
    if root is None:
        return TreeNode(value)

    if value < root.value:
        root.left = bst_insert(root.left, value)
    else:
        root.right = bst_insert(root.right, value)

    return root


def bst_search(root: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
    """
    Searches for a value in the Binary Search Tree (BST).

    Args:
        root (Optional[TreeNode]): The root of the BST.
        value (Any): The value to search for.

    Returns:
        Optional[TreeNode]: The node containing the value, or None if not found.
    """
    if root is None or root.value == value:
        return root

    if value < root.value:
        return bst_search(root.left, value)
    else:
        return bst_search(root.right, value)


def bst_delete(root: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
    """
    Deletes a value from the Binary Search Tree (BST).

    Args:
        root (Optional[TreeNode]): The root node of the BST.
        value (Any): The value to delete.

    Returns:
        Optional[TreeNode]: The root node of the BST after deletion.
    """
    if root is None:
        return None

    if value < root.value:
        root.left = bst_delete(root.left, value)
    elif value > root.value:
        root.right = bst_delete(root.right, value)
    else:
        # Node with only one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Node with two children: Get the inorder successor
        min_larger_node = bst_find_min(root.right)
        root.value = min_larger_node.value
        root.right = bst_delete(root.right, min_larger_node.value)

    return root


def bst_find_min(root: TreeNode) -> TreeNode:
    """
    Finds the node with the minimum value in a BST.

    Args:
        root (TreeNode): The root node of the BST.

    Returns:
        TreeNode: The node with the minimum value.
    """
    current = root
    while current.left is not None:
        current = current.left
    return current
