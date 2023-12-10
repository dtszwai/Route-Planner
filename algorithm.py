def dijkstra(matrix):
    if matrix is None:
        return None

    nodes = [i for i in range(1, len(matrix))]

    visited = [0]
    distance = {0: 0}

    path = [0]
    curr_node = 0

    while nodes:
        mid_distance = float("inf")
        for v in visited:
            for node in nodes:
                new_distance = matrix[0][v] + matrix[v][node]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    curr_node = node
        distance[curr_node] = mid_distance
        path.append(curr_node)

        visited.append(curr_node)
        nodes.remove(curr_node)

    return path


def dp(matrix):
    n = len(matrix)
    all_cities = set(range(n - 1))

    memo = {}

    def tsp_dp_helper(curr, visited):
        if not visited:
            return matrix[curr][n - 1]

        key = (curr, tuple(visited))
        if key in memo:
            return memo[key]

        min_cost = float("inf")
        for next_city in visited:
            new_visited = visited - {next_city}
            cost = matrix[curr][next_city] + tsp_dp_helper(next_city, new_visited)
            min_cost = min(min_cost, cost)

        memo[key] = min_cost
        return min_cost

    optimal_cost = tsp_dp_helper(n - 1, all_cities)

    path = [n - 1]
    curr_city = n - 1
    remaining_cities = all_cities.copy()

    for _ in range(n - 1):
        next_city = min(remaining_cities, key=lambda x: matrix[curr_city][x])
        path.append(next_city)
        remaining_cities.remove(next_city)
        curr_city = next_city

    optimal_distance = optimal_cost - matrix[path[-1]][n - 1]
    path.reverse()
    return path
