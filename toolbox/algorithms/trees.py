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


def bst_lowest_common_ancestor(
    root: Optional[TreeNode], p: Any, q: Any
) -> Optional[TreeNode]:
    """
    Finds the Lowest Common Ancestor (LCA) of two values in a BST.

    Args:
        root (Optional[TreeNode]): The root node of the BST.
        p (Any): The first value.
        q (Any): The second value.

    Returns:
        Optional[TreeNode]: The LCA node, or None if not found.
    """
    if root is None:
        return None

    if p < root.value and q < root.value:
        return bst_lowest_common_ancestor(root.left, p, q)
    elif p > root.value and q > root.value:
        return bst_lowest_common_ancestor(root.right, p, q)
    else:
        return root


def bt_lowest_common_ancestor(
    root: Optional[TreeNode], p: Any, q: Any
) -> Optional[TreeNode]:
    """
    Finds the Lowest Common Ancestor (LCA) of two values in a binary tree.

    Args:
        root (Optional[TreeNode]): The root node of the binary tree.
        p (Any): The first value.
        q (Any): The second value.

    Returns:
        Optional[TreeNode]: The LCA node, or Node if not found.
    """
    if root is None or root.value == p or root.value == q:
        return root

    left = bt_lowest_common_ancestor(root.left, p, q)
    right = bt_lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right


def build_tree_from_in_pre(
    inorder: list[Any], preorder: list[Any]
) -> Optional[TreeNode]:
    """
    Builds a binary tree from inorder and preorder traversals.

    Args:
        inorder (list[Any]): The inorder traversal sequence.
        preorder (list[Any]): The preorder traversal sequence.

    Returns:
        Optional[TreeNode]: The root node of the reconstructed tree.
    """
    if not inorder or not preorder:
        return None

    root_value = preorder[0]
    root = TreeNode(root_value)

    inorder_index = inorder.index(root_value)

    root.left = build_tree_from_in_pre(
        inorder[:inorder_index], preorder[1 : inorder_index + 1]
    )
    root.right = build_tree_from_in_pre(
        inorder[inorder_index + 1 :], preorder[inorder_index + 1 :]
    )

    return root


def build_tree_from_in_post(
    inorder: list[Any], postorder: list[Any]
) -> Optional[TreeNode]:
    """
    Builds a binary tree from inorder and postorder traversals.

    Args:
        inorder (list[Any]): The inorder traversal sequence.
        postorder (list[Any]): The postorder traversal sequence.

    Returns:
        Optional[TreeNode]: The root node of the reconstructed tree.
    """
    if not inorder or not postorder:
        return None

    root_value = postorder[-1]
    root = TreeNode(root_value)

    inorder_index = inorder.index(root_value)

    root.left = build_tree_from_in_post(
        inorder[:inorder_index], postorder[:inorder_index]
    )
    root.right = build_tree_from_in_post(
        inorder[inorder_index + 1 :], postorder[inorder_index:-1]
    )

    return root


def tree_height(root: Optional[TreeNode]) -> int:
    """
    Calculates the height of a binary tree.

    Args:
        root (Optional[TreeNode]): The root node if the tree.

    Returns:
        int: The height of the tree.
    """
    if root is None:
        return -1

    left_height = tree_height(root.left)
    right_height = tree_height(root.right)
    return 1 + max(left_height, right_height)


def tree_size(root: Optional[TreeNode]) -> int:
    """
    Calculates the number of nodes in a binary tree.

    Args:
        root: (Optional[TreeNode]): The root node of the tree.

    Returns:
        int: The total number of nodes.
    """
    if root is None:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)


def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    Determines if a binary tree is height-balanced.

    Args:
        root (Optional[TreeNode]): The root node of the tree.

    Returns:
        bool: True if the tree is balanced, False otherwise.
    """

    def check(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_height = check(node.left)
        if left_height == -1:
            return -1
        right_height = check(node.right)
        if right_height == -1:
            return -1
        if abs(left_height - right_height) > 1:
            return -1
        return 1 + max(left_height, right_height)

    return check(root) != -1
