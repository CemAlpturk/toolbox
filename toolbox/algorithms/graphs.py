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


def tarjan_scc(graph: Graph) -> list[list[Any]]:
    """
    Finds strongly connected components in a directed graph using Tarjan's algorithm.

    Args:
        graph (Graph): The graph represented as an adjacency list.

    Returns:
        list[list[Any]]: A list of strongly connected components, each component is a list of nodes.
    """

    index = 0
    indices: dict[Any, int] = {}
    lowlink: dict[Any, int] = {}
    stack: list[Any] = []
    on_stack: set[Any] = set()
    sccs: list[list[Any]] = []

    def strongconnect(node: Any) -> None:
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.adj_list.get(node, []):
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], indices[neighbor])

        # If node is a root nod, pop the stack and generate an SCC
        if lowlink[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    for node in graph.nodes():
        if node not in indices:
            strongconnect(node)

    return sccs


def kruskal_mst(graph: Graph) -> list[tuple[Any, Any, float]]:
    """
    Computes the Minimum Spanning Tree (MST) of a connected, undirected graph using Kruskal's algorithm.

    Args:
        graph (Graph): A weighted undirected graph.

    Returns:
        list[tuple[Any, Any, float]]: The edges in the MST.
    """

    parent: dict[Any, Any] = {}
    rank: dict[Any, int] = {}

    def find(u: Any) -> Any:
        if parent.get(u, u) != u:
            parent[u] = find(parent[u])
        return parent.get(u, u)

    def union(u: Any, v: Any) -> None:
        u_root = find(u)
        v_root = find(v)
        if u_root == v_root:
            return
        if rank.get(u_root, 0) < rank.get(v_root, 0):
            parent[u_root] = v_root
        else:
            parent[v_root] = u_root
            if rank.get(u_root, 0) == rank.get(v_root, 0):
                rank[u_root] = rank.get(u_root, 0) + 1

    # Extract graph edges
    _graph_edges: set[tuple[Any, Any, float]] = set()
    for u in graph.nodes():
        for v in graph.adj_list.get(u, []):
            w = graph.weights[(u, v)]
            _graph_edges.add((u, v, w))
    graph_edges = list(_graph_edges)

    # Sort edges by weight
    sorted_edges = sorted(graph_edges, key=lambda edge: edge[2])
    mst_edges: list[tuple[Any, Any, float]] = []

    for u, v, w in sorted_edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, w))

    return mst_edges


def bellman_ford(graph: Graph, start: Any) -> dict[Any, float] | None:
    """
    Computes the shortest paths from the start node to all other nodes in a weighted graph using the Bellman-Fort algorithm.
    Can handle graphs with negative weight edges.

    Args:
        graph (Graph): The graph represented as an adjacency list.
        start (Any): The starting node.

    Returns:
        dict[Any, float] | None: A dictionary mapping the nodes to their shortest distance from the start node.
        Returns None if a negative cycle is detected.
    """

    distances: dict[Any, float] = defaultdict(lambda: float("inf"))
    distances[start] = 0.0

    # Flatten the graph edges
    edges: list[tuple[Any, Any, float]] = []
    for u in graph.nodes():
        for v, w in graph.adj_list.get(u, []):
            edges.append((u, v, w))

    # Relax edges repeadetly
    # PERF: Not the most optimal way of handling this
    num_vertices = len(list(graph.nodes()))
