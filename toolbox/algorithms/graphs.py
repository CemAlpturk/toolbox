from typing import (
    Any,
    Callable,
)
from collections import defaultdict


from toolbox.data_structures import (
    Graph,
    PriorityQueue,
)


def bfs(graph: Graph, start: Any) -> list[Any]:
    """
    Performs Breadth-First Search on a graph.

    Args:
        graph (Graph): The graph represented as an adjacency list.
        start (Any): The starting node.

    Returns:
        list[Any]: A list of nodes in the order they were visited.
    """
    visited: set[Any] = set()
    queue: list[Any] = [start]
    order: list[Any] = []

    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            for u in graph.adj_list.get(vertex, []):
                if u not in visited:
                    queue.append(u)

    return order


def dfs(graph: Graph, start: Any) -> list[Any]:
    """
    Performs Depth-First Search on a graph.

    Args:
        graph (Graph): The graph represented as an adjacency list.
        start (Any): The starting node.

    Returns:
        list[Any]: A list of nodes in the order they were visited.
    """
    visited: set[Any] = set()
    order: list[Any] = []

    def dfs_recursive(node: Any):
        visited.add(node)
        order.append(node)
        for u in graph.adj_list.get(node, []):
            if u not in visited:
                dfs_recursive(u)

    dfs_recursive(start)
    return order


def dijkstra(graph: Graph, start: Any) -> dict[Any, float]:
    """
    Computes the shortest paths from the start node to all other nodes in a weighted graph using Dijkstra's algorithm.

    Args:
        graph (Graph): The graph represented as an adjacency list with weights.
        start (Any): The starting node.

    Returns:
        dict[Any, float]: A dictionary mapping nodes to their shortest distance from the start node.
    """
    distances: dict[Any, float] = defaultdict(lambda: float("inf"))
    distances[start] = 0.0
    priority_queue: PriorityQueue = PriorityQueue([(0.0, start)], lambda x: x[0])
    visited: set[Any] = set()

    while priority_queue:
        current_distance, current_node = priority_queue.pop()

        if current_node in visited:
            continue
        visited.add(current_node)

        for v in graph.adj_list.get(current_node, []):
            w = graph.weights[(current_node, v)]
            distance = current_distance + w
            if distance < distances[v]:
                distances[v] = distance
                priority_queue.push((distance, v))

    return distances


def a_start_search(
    graph: Graph,
    start: Any,
    goal: Any,
    heuristic: Callable[[Any, Any], float],
) -> list[Any] | None:
    """
    Finds the shortest path between start and goal nodes using the A* search algorithm.

    Args:
        graph (Graph): The graph represented as an adjacency list with weights.
        start (Any): The starting node.
        goal (Any): The goal node.
        heuristic (Callable[[Any, Any], float]): A function that estimates the cost from a node to the goal.

    Returns:
        list[Any] | None: The shortest path from start to goal as a list of nodes, or None if no path exists.
    """
    open_set: set[Any] = set([start])
    came_from: dict[Any, Any] = {}
    g_score: dict[Any, float] = defaultdict(lambda: float("inf"))
    g_score[start] = 0.0
    f_score: dict[Any, float] = defaultdict(lambda: float("inf"))
    f_score[start] = heuristic(start, goal)

    priority_queue: PriorityQueue = PriorityQueue(
        [(f_score[start], start)], key=lambda x: x[0]
    )

    while priority_queue:
        _, current_node = priority_queue.pop()

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        open_set.discard(current_node)

        for v in graph.adj_list.get(current_node, []):
            w = graph.weights[(current_node, v)]
            tentative_g_score = g_score[current_node] + w
            if tentative_g_score < g_score[v]:
                came_from[v] = current_node
                g_score[v] = tentative_g_score
                f_score[v] = tentative_g_score + heuristic(v, goal)
                if v not in open_set:
                    open_set.add(v)
                    priority_queue.push((f_score[v], v))

    return None


def reconstruct_path(came_from: dict[Any, Any], current: Any) -> list[Any]:
    """
    Reconstructs the path from start to goal.

    Args:
        came_from (dict[Any, Any]): A mapping of nodes to their predecessors.
        current (Any): The current node.

    Returns:
        list[Any]: The reconstructed path.
    """

    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def topological_sort(graph: Graph) -> list[Any]:
    """
    Performs a topological sort on a Directed Acyclic Graph (DAG).

    Args:
        graph (Graph): The graph represented as an adjacency list.

    Returns:
        list[Any]: A list of nodes in topologically sorted order.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    visited: set[Any] = set()
    temp_marked: set[Any] = set()
    order: list[Any] = []

    def visit(node: Any) -> None:
        if node in temp_marked:
            raise ValueError("Graph is not a DAG (contains a cycle)")
        if node not in visited:
            temp_marked.add(node)
            for v in graph.adj_list.get(node, []):
                visit(v)
            temp_marked.remove(node)
            visited.add(node)
            order.append(node)

    for node in graph.nodes():
        if node not in visited:
            visit(node)

    return order[::-1]
