import os
import sys
import streamlit as st
from dotenv import load_dotenv
from algorithm import dijkstra, dp
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


def get_travel_route(cities_info, data_source=GOOGLE_MAPS, algorithm=dijkstra):
    if data_source == GOOGLE_MAPS:
        distance_matrix = get_distance_matrix_by_google_maps(cities_info)
    elif data_source == COORDINATE:
        distance_matrix = get_distance_matrix_by_coordinate(cities_info)

    path_order = algorithm(distance_matrix)
    ordered_cities_info = [cities_info[i] for i in path_order]

    total_distance = sum(
        distance_matrix[i][j] for i, j in zip(path_order, path_order[1:])
    )

    return ordered_cities_info, total_distance


def visualizer(ordered_cities_info, distance, title):
    route = [f"`{city[0]}`" for city in ordered_cities_info]
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


def parse_command_line(arguments):
    if len(arguments) > 1:
        city_file_path = arguments[1]
        method = arguments[2] if len(arguments) > 2 else GOOGLE_MAPS
    else:
        city_file_path = "city.txt"
        method = GOOGLE_MAPS
    return city_file_path, method


def read_cities_info(file_path):
    return [tuple(line.strip().split(",")) for line in open(file_path, "r")]


def run_and_visualize_algorithm(cities_info, data_source, algorithm, title):
    ordered_cities_info, total_distance = get_travel_route(
        cities_info=cities_info, data_source=data_source, algorithm=algorithm
    )
    visualizer(ordered_cities_info, total_distance, title=title)


def main():
    city_file_path, data_source = parse_command_line(sys.argv)
    cities_info = read_cities_info(city_file_path)

    st.title(f"Shortest Travel Route Visualizer")
    st.markdown(f"Calculating distances using `{data_source.capitalize()}`.")

    run_and_visualize_algorithm(
        cities_info=cities_info,
        data_source=data_source,
        algorithm=dijkstra,
        title="Dijkstra's Algorithm",
    )
    run_and_visualize_algorithm(
        cities_info=cities_info,
        data_source=data_source,
        algorithm=dp,
        title="Dynamic Programming",
    )


if __name__ == "__main__":
    main()
