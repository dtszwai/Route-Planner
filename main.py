import os
import sys
from dijkstra import dijkstra
from dotenv import load_dotenv
from tsp import tsp
import streamlit as st
from distance import (
    get_distance_matrix_by_google_maps,
    get_distance_matrix_by_coordinate,
)

GOOGLE_MAPS = "google_maps"
COORDINATE = "coordinate"

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


def get_map_url(cities):
    city_info = [f"{city[0]}, {city[1]}, {city[2]}" for city in cities]
    waypoints = "|".join(city_info[1:-1])

    url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAP_API_KEY}&origin={city_info[0]}&destination={city_info[-1]}&waypoints={waypoints}&mode=driving"

    return url


def get_travel_route(path, method=GOOGLE_MAPS, algorithm=dijkstra):
    cities_info = []

    with open(path, "r") as file:
        for line in file:
            city, state, country = line.strip().split(",")
            cities_info.append((city, state, country))

    if method == GOOGLE_MAPS:
        distance_matrix = get_distance_matrix_by_google_maps(cities_info)
    elif method == COORDINATE:
        distance_matrix = get_distance_matrix_by_coordinate(cities_info)

    path_order = algorithm(distance_matrix)
    ordered_cities_info = [cities_info[i] for i in path_order]

    total_distance = sum(
        distance_matrix[i][j] for i, j in zip(path_order, path_order[1:])
    )

    return ordered_cities_info, total_distance


def visualizer(cities, distance, title):
    route = [f"`{city[0]}`" for city in cities]
    formatted_route = " -> ".join(route)

    map_url = get_map_url(ordered_cities_info)

    st.header(f"Travel Route ({title}):")
    st.write(
        f"<span style='font-size:1.5em'>{formatted_route}</span>",
        unsafe_allow_html=True,
    )
    st.write(f"Total Distance: {int(distance)} km")

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
    if len(sys.argv) > 1:
        city_file_path = sys.argv[1]
        method = sys.argv[2] if len(sys.argv) > 2 else GOOGLE_MAPS
    else:
        print("Usage: streamlit main.py [city_file_path] [method]")
        sys.exit(1)

    st.title(f"Shortest Travel Route Visualizer")
    st.markdown(f"Calculating distances using `{method.capitalize()}`.")

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, method=method, algorithm=dijkstra
    )

    visualizer(ordered_cities_info, total_distance, title="Dijkstra")

    ordered_cities_info, total_distance = get_travel_route(
        path=city_file_path, method=method, algorithm=tsp
    )
    visualizer(ordered_cities_info, total_distance, title="TSP")
