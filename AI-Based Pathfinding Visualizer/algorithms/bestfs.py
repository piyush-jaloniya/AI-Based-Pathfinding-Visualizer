import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def best_first_search(grid, start, end):
    if start == end:
        return [start]

    rows, cols = len(grid), len(grid[0])
    visited = set()
    parent = {}
    heap = [(heuristic(start, end), start)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while heap:
        _, current = heapq.heappop(heap)
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if current in visited:
            continue
        visited.add(current)

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(heap, (heuristic(neighbor, end), neighbor))

    return None
