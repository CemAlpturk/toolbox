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
