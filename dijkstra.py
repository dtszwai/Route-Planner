def dijkstra(graph, src=0):
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]
    visited = []
    if src in nodes:
        visited.append(src)
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}
    for i in nodes:
        distance[i] = graph[src][i]
    path = {src: {src: []}}
    k = pre = src
    while nodes:
        mid_distance = float("inf")
        for v in visited:
            for d in nodes:
                new_distance = graph[src][v] + graph[v][d]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    graph[src][d] = new_distance
                    k = d
                    pre = v
        distance[k] = mid_distance
        path[src][k] = [i for i in path[src][pre]]
        path[src][k].append(k)

        visited.append(k)
        nodes.remove(k)
    return path[src]
