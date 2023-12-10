import sys
import requests
from geopy.distance import geodesic
from dijkstra import dijkstra
from tsp import tsp
import streamlit as st


OPEN_WEATHER_MAP_API_KEY = ""
GOOGLE_MAP_API_KEY = ""


def get_location(city="", state="", country="", limit=1):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={OPEN_WEATHER_MAP_API_KEY}"
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
    city_info = [f"{city[0]}, {city[1]}, {city[2]}" for city in cities]
    waypoints = "|".join(city_info[1:-1])

    url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAP_API_KEY}&origin={city_info[0]}&destination={city_info[-1]}&waypoints={waypoints}&mode=driving"

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


def visualizer(cities, distance, title):
    route = [city[0] for city in cities]
    formatted_route = " -> ".join(route)

    map_url = get_map_url(ordered_cities_info)

    st.header(f"Travel Route ({title}):")
    st.write(formatted_route)
    st.write(f"Total Distance: {distance}")

    embed_code = f"""
        <iframe
            width="600"
            height="450"
            style="border:0"
            src="{map_url}"
            allowfullscreen
        >
        </iframe>
    """

    st.components.v1.html(embed_code, height=500)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        city_file_path = sys.argv[1]
    elif len(sys.argv) == 1:
        city_file_path = "city.txt"
    else:
        print("Usage: streamlit main.py [city_file_path]")
        sys.exit(1)

    st.title("Shortest Travel Route Visualizer")

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, algorithm=dijkstra
    )

    visualizer(ordered_cities_info, total_distance, title="Dijkstra")

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, algorithm=tsp
    )
    visualizer(ordered_cities_info, total_distance, title="TSP")
