def dijkstra(matrix, reverse=False):
    n = len(matrix)
    start, destination = (n - 1, 0) if reverse else (0, n - 1)

    remaining_cities = (
        list(range(start + 1, destination))
        if not reverse
        else list(range(destination + 1, start))
    )

    total_distance = 0
    path = [start]
    curr_city = start

    while remaining_cities:
        next_city = min(remaining_cities, key=lambda x: matrix[curr_city][x])
        path.append(next_city)
        total_distance += matrix[curr_city][next_city]
        curr_city = next_city
        remaining_cities.remove(next_city)

    path.append(destination)
    total_distance += matrix[curr_city][destination]

    if reverse:
        path.reverse()

    return path, total_distance
