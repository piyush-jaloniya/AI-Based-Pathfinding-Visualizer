def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def hill_climbing(grid, start, end):
    if start == end:
        return [start]

    rows, cols = len(grid), len(grid[0])
    visited = set()
    parent = {}
    current = start

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while current != end:
        neighbors = []
        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                neighbors.append((heuristic(neighbor, end), neighbor))

        if not neighbors:
            return None  # No valid moves (local minimum)

        next_node = min(neighbors, key=lambda x: x[0])[1]

        parent[next_node] = current
        current = next_node
        visited.add(current)

    path = []
    while current in parent:
        path.append(current)
        current = parent[current]

    return path[::-1]
