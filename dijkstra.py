def dijkstra(graph, src=0):
    if graph is None:
        return None

    nodes = [i for i in range(1, len(graph))]

    visited = [0]
    distance = {src: 0}

    path = [0]
    curr_node = src

    while nodes:
        mid_distance = float("inf")
        for v in visited:
            for node in nodes:
                new_distance = graph[src][v] + graph[v][node]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    curr_node = node
        distance[curr_node] = new_distance
        path.append(curr_node)

        visited.append(curr_node)
        nodes.remove(curr_node)

    return path
