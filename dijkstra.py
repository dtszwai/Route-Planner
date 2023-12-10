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
