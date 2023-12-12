import os
import sys
import streamlit as st
from dotenv import load_dotenv
from algorithm import dijkstra
from distance import (
    get_distance_matrix_by_google_maps,
    get_distance_matrix_by_coordinate,
)

# Data Sources
GOOGLE_MAPS = "google_maps"
COORDINATE = "coordinate"

load_dotenv()

# Get API key from .env
GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


def get_map_url(cities):
    """
    Generate a Google Maps URL for the given list of cities.

    Parameters:
    - cities (list): A list of tuples, where each tuple represents a city with the format
      ('City Name', 'State/Province', 'Country Code').

    Returns:
    str: The Google Maps URL with directions based on the provided city information.
    """
    # Constructing the URL with origin, destination, and waypoints
    formatted_cities = [f"{city[0]}, {city[1]}, {city[2]}" for city in cities]
    waypoints = "|".join(formatted_cities[1:-1])

    url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAP_API_KEY}&origin={formatted_cities[0]}&destination={formatted_cities[-1]}&waypoints={waypoints}&mode=driving"

    return url


def get_travel_route(
    cities, data_source=GOOGLE_MAPS, algorithm=dijkstra, reverse=False
):
    """
    Calculate the travel route using the specified algorithm and data source.

    Parameters:
    - cities (list): A list of tuples, where each tuple represents a city with the format
      ('City Name', 'State/Province', 'Country Code').
    - data_source (str): The data source for calculating distances, either 'google_maps' or 'coordinate'.
    - algorithm (function): The algorithm to use for finding the travel route.
    - reverse (bool): If True, reverse the calculated route.

    Returns:
    tuple: A tuple containing two elements:
        - list: Ordered list of cities representing the travel route.
        - float: Total distance of the travel route.
    """
    if data_source == GOOGLE_MAPS:
        distance_matrix = get_distance_matrix_by_google_maps(cities)
    elif data_source == COORDINATE:
        distance_matrix = get_distance_matrix_by_coordinate(cities)

    path_order, total_distance = algorithm(distance_matrix, reverse)
    ordered_cities = [cities[i] for i in path_order]

    return ordered_cities, total_distance


def visualizer(ordered_cities, distance, title):
    """
    Display the travel route on Streamlit with a map.

    Parameters:
    - ordered_cities (list): Ordered list of tuple of cities representing the travel route.
    - distance: Total distance of the travel route.
    - title (str): The title for the visualization.
    """
    # Format route information
    route = [f"`{city[0]}`" for city in ordered_cities]
    formatted_route = " -> ".join(route)

    # Get the Google Maps embed URL
    map_url = get_map_url(ordered_cities)

    # Display route information and embed the map
    st.header(f"Travel Route ({title}):")
    st.write(
        f"<span style='font-size:1.5em'>{formatted_route}</span>",
        unsafe_allow_html=True,
    )
    st.write(f"Total Distance: {round(distance)} km")

    embed_code = f"""
        <iframe
            width="100%"
            height="480px"
            style="border:0"
            src="{map_url}"
            allowfullscreen
        >
        </iframe>
    """

    st.components.v1.html(embed_code, height=500)


def parse_command_line(arguments):
    """
    Parse command line arguments to get the city file path and data source.

    Parameters:
    - arguments (list): List of command line arguments.

    Returns:
    tuple: A tuple containing two elements:
        - str: File path for the city information.
        - str: Data source for calculating distances.
    """

    if len(arguments) > 1:
        city_file_path = arguments[1]
        method = arguments[2] if len(arguments) > 2 else GOOGLE_MAPS
    else:
        city_file_path = "city.txt"
        method = GOOGLE_MAPS
    return city_file_path, method


def read_cities_info(file_path):
    """
    Read city information from a file and return a list of tuples.

    Parameters:
    - file_path (str): The path to the file containing city information.

    Returns:
    list: A list of tuples representing city information.
    """
    return [tuple(line.strip().split(",")) for line in open(file_path, "r")]


def run_and_visualize_algorithm(cities, data_source, algorithm, title, reverse=False):
    """
    Run the algorithm, visualize the result, and display on Streamlit.

    Parameters:
    - cities (list): A list of tuples representing city information.
    - data_source (str): The data source for calculating distances, either 'google_maps' or 'coordinate'.
    - algorithm (function): The algorithm to use for finding the travel route.
    - title (str): The title for the visualization.
    - reverse (bool): If True, reverse the calculated route.
    """
    ordered_cities, total_distance = get_travel_route(
        cities=cities,
        data_source=data_source,
        algorithm=algorithm,
        reverse=reverse,
    )
    visualizer(ordered_cities, total_distance, title=title)


def main():
    """Main function to run the program."""
    # Parse command line arguments
    city_file_path, data_source = parse_command_line(sys.argv)
    cities = read_cities_info(city_file_path)

    # Display Streamlit app title and information
    st.title(f"Shortest Travel Route Visualizer")
    st.markdown(f"Calculating distances using `{data_source.capitalize()}`.")

    # Run and visualize the algorithm with and without reverse order
    run_and_visualize_algorithm(
        cities=cities,
        data_source=data_source,
        algorithm=dijkstra,
        title="Dijkstra's Algorithm",
    )
    run_and_visualize_algorithm(
        cities=cities,
        data_source=data_source,
        algorithm=dijkstra,
        reverse=True,
        title="Dijkstra's Algorithm (Reverse)",
    )


if __name__ == "__main__":
    main()
