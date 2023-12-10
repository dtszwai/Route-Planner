import sys
import requests
from geopy.distance import geodesic
from dijkstra import dijkstra
from rich.console import Console
from rich.table import Table
from tsp import tsp


API_KEY = ""


def get_location(city="", state="", country="", limit=1):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={API_KEY}"
    response = requests.get(url)
    response_json = response.json()
    location = [response_json[0]["lat"], response_json[0]["lon"]]
    return location


def get_distance_matrix(cities_location: dict[list]):
    cities = list(cities_location.keys())

    distance_matrix = [[0] * len(cities) for _ in range(len(cities))]

    for i in range(len(cities)):
        for j in range(len(cities)):
            if i == j:
                distance_matrix[i][j] = 0
            else:
                city1_location = cities_location[cities[i]]
                city2_location = cities_location[cities[j]]

                distance_matrix[i][j] = int(geodesic(city1_location, city2_location).km)

    return distance_matrix


def get_map_url(cities):
    url = "https://www.google.com/maps/dir/"
    for city in cities:
        city_name = city[0].replace(" ", "+")
        state = city[1].replace(" ", "+")
        country = city[2].replace(" ", "+")

        params = f"{city_name},{state},{country}/"
        url += params
    return url


def get_travel_route(path, algorithm=dijkstra):
    cities_info = []
    city_location_mapping = {}

    with open(path, "r") as file:
        for line in file:
            city, state, country = line.strip().split(",")
            cities_info.append((city, state, country))

    for city in cities_info:
        location = get_location(*city)
        city_location_mapping[city] = location

    distance_matrix = get_distance_matrix(city_location_mapping)
    path_order = algorithm(distance_matrix)
    ordered_cities_info = [cities_info[i] for i in path_order]

    total_distance = sum(
        distance_matrix[i][j] for i, j in zip(path_order, path_order[1:])
    )

    return ordered_cities_info, total_distance


def print_result(cities, distance, title):
    console = Console()

    route = [city[0] for city in cities]
    formatted_route = " -> ".join(route)

    map_url = get_map_url(ordered_cities_info)

    table = Table(expand=True)
    table.add_column(f"Travel Route ({title})", justify="center", style="bold cyan")

    table.add_row(f"[green]Total Distance: {str(distance)}km[/green]")
    table.add_row(f"[blue]{formatted_route}[/blue]")
    table.add_row(
        f"[yellow][link={map_url}]Google Maps Route: [/link][/yellow] {map_url}"
    )

    console.print(table)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        city_file_path = sys.argv[1]
    elif len(sys.argv) == 1:
        city_file_path = "city.txt"
    else:
        print("Usage: python3 main.py [city_file_path]")
        sys.exit(1)

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, algorithm=dijkstra
    )
    print_result(ordered_cities_info, total_distance, title="Dijkstra")

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, algorithm=tsp
    )
    print_result(ordered_cities_info, total_distance, title="TSP")
