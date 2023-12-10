def tsp(matrix):
    n = len(matrix)
    all_cities = set(range(1, n))

    memo = {}

    def tsp_dp_helper(curr, visited):
        if not visited:
            return matrix[curr][0]

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

    optimal_cost = tsp_dp_helper(0, all_cities)

    path = [0]
    curr_city = 0
    remaining_cities = all_cities.copy()

    for _ in range(n - 1):
        next_city = min(remaining_cities, key=lambda x: matrix[curr_city][x])
        path.append(next_city)
        remaining_cities.remove(next_city)
        curr_city = next_city

    optimal_distance = optimal_cost - matrix[path[-1]][0]

    return path
