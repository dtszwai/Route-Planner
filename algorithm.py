def dijkstra(matrix):
    num_nodes = len(matrix)
    destination = num_nodes - 1

    nodes = set(range(1, destination)) # All waypoints are nodes

    total_distance = 0
    path = [0]
    curr_node = 0

    while nodes:
        next_node, min_distance = min(
            ((node, matrix[curr_node][node]) for node in nodes), key=lambda x: x[1]
        )
        total_distance += min_distance
        curr_node = next_node
        path.append(next_node)
        nodes.remove(next_node)

    path.append(destination)
    total_distance += matrix[curr_node][destination]

    return path, total_distance


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
    return path, optimal_distance
