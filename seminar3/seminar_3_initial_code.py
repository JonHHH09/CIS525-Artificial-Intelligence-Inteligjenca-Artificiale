import heapq


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic cost from current node to end node
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f


def a_star_search(graph, start, end):
    """
    Implements the A* search algorithm.

    Args:
        graph (dict): A dictionary representing the graph where keys are nodes
                      and values are lists of connected nodes and their costs.
                      Example: {'A': [('B', 1), ('C', 3)], 'B': [('D', 2)], ...}
        start (str): The starting node.
        end (str): The destination node.

    Returns:
        list: The path from start to end if found, otherwise None.
    """
    start_node = Node(start) # starts the node
    end_node = Node(end) # starts the end node

    open_list = [] # stores the nodes to be evaluated
    closed_list = set() # stores the nodes that have been evaluated

    heapq.heappush(open_list, start_node) # pushes the start node onto the open list

    while open_list: # while loop for the open list
        current_node = heapq.heappop(open_list) # pops the node with the lowest f value from the open list
        closed_list.add(current_node.position) # adds the current node to the closed list

        if current_node.position == end_node.position: # checks if the current node is the end node
            path = [] # stores the path from start to end
            while current_node is not None: # checks if the current node is not None
                path.append(current_node.position) # adds the current node to the path
                current_node = current_node.parent # moves to the parent node
            return path[::-1]  # Return reversed path

        if current_node.position in graph:
            for neighbor_pos, cost in graph[current_node.position]:
                if neighbor_pos in closed_list:
                    continue

                neighbor = Node(neighbor_pos, current_node)
                neighbor.g = current_node.g + cost
                # For a basic example, we can use Manhattan distance or a simple
                # straight-line distance as a heuristic if coordinates are available.
                # Here, we'll use a placeholder heuristic (e.g., 0 for simplicity,
                # or a pre-calculated value if a more informed heuristic is desired).
                neighbor.h = 0  # Placeholder heuristic
                neighbor.f = neighbor.g + neighbor.h

                # Check if neighbor is already in open_list with a higher f value
                in_open_list = False
                for node_in_open in open_list:
                    if neighbor.position == node_in_open.position and neighbor.f >= node_in_open.f:
                        in_open_list = True
                        break

                if not in_open_list:
                    heapq.heappush(open_list, neighbor)

    return None  # Path not found


# Define a simple graph (module level so seminar3/draw.py can draw it)
graph_data = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 4)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'F': [],
    'G': []
}


# Example Usage:
if __name__ == "__main__":
    start_node_name = 'A'
    end_node_name = 'G'

    path_found = a_star_search(graph_data, start_node_name, end_node_name)

    if path_found:
        print(f"Path from {start_node_name} to {end_node_name}: {path_found}")
    else:
        print(f"No path found from {start_node_name} to {end_node_name}.")
