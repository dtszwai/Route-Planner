def knn(matrix):
    """
    Find the shortest path using Nearest neighbour algorithm on a given distance matrix.

    Parameters:
    - matrix (list): A 2D list representing the distance matrix between cities.

    Returns:
    tuple: A tuple containing two elements:
        - list: The ordered list of cities representing the shortest path.
        - float: The total distance of the shortest path.
    """

    # Number of cities
    n = len(matrix)

    # Define start and destination
    start, destination = 0, n - 1

    # Initialize remaining cities to visit
    remaining_cities = list(range(start + 1, destination))

    # Initialize variables for the total distance and the path
    total_distance = 0
    path = [start]
    curr_city = start

    # Main loop of Nearest neighbour algorithm
    while remaining_cities:
        # Find the next city with the minimum distance
        next_city = min(remaining_cities, key=lambda x: matrix[curr_city][x])

        # Update path and total distance
        path.append(next_city)
        total_distance += matrix[curr_city][next_city]

        # Move to the next city
        curr_city = next_city
        remaining_cities.remove(next_city)

    # Add the destination city to the path and update total distance
    path.append(destination)
    total_distance += matrix[curr_city][destination]

    return path, total_distance
