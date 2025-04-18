import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, end):
    if start == end:
        return [start]

    rows, cols = len(grid), len(grid[0])
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    heap = [(f_score[start], start)]
    parent = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while heap:
        _, current = heapq.heappop(heap)
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(heap, (f_score[neighbor], neighbor))
                    parent[neighbor] = current

    return None  # No path found
