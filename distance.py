import os
import requests
from geopy.distance import geodesic
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_distance_matrix_by_google_maps(cities):
    """
    Get the distance matrix between cities using Google Maps Distance Matrix API.

    Parameters:
    - cities (list): A list of tuples, where each tuple represents a city with the format
      ('City Name', 'State/Province', 'Country Code').

    Returns:
    list: A 2D list representing the distance matrix between cities (in kilometers).
    """
    formatted_cities = "%7C".join(
        [
            f"{city.replace(' ', '%20')},{state.replace(' ', '%20')},{country}"
            for city, state, country in cities
        ]
    )

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={formatted_cities}&origins={formatted_cities}&units=imperial&key={GOOGLE_MAPS_API_KEY}"

    response = requests.get(url)
    response_json = response.json()

    # Initialize the distance matrix with zeros
    distance_matrix = [[0] * len(cities) for _ in range(len(cities))]

    # Populate the distance matrix with values from the API response
    for i, row in enumerate(response_json["rows"]):
        for j, element in enumerate(row["elements"]):
            value = element["distance"]["value"]  # meters
            distance_matrix[i][j] = value / 1000  # convert to km

    return distance_matrix


def get_distance_matrix_by_coordinate(cities):
    """
    Get the distance matrix between cities using geographic coordinates.

    Parameters:
    - cities (list): A list of tuples, where each tuple represents a city with the format
      ('City Name', 'State/Province', 'Country Code').

    Returns:
    list: A 2D list representing the distance matrix between cities (in kilometers).
    """
    city_location_mapping = {}

    def get_location(city="", state="", country="", limit=1):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={OPEN_WEATHER_MAP_API_KEY}"
        response = requests.get(url)
        response_json = response.json()
        location = [response_json[0]["lat"], response_json[0]["lon"]]
        return location

    def get_distance_matrix(cities_location: dict[list]):
        cities = list(cities_location.keys())

        # Initialize the distance matrix with zeros
        distance_matrix = [[0] * len(cities) for _ in range(len(cities))]

        # Populate the distance matrix with geodesic distances
        for i in range(len(cities)):
            for j in range(len(cities)):
                if i == j:
                    distance_matrix[i][j] = 0
                else:
                    city1_location = cities_location[cities[i]]
                    city2_location = cities_location[cities[j]]

                    distance_matrix[i][j] = int(
                        geodesic(city1_location, city2_location).km
                    )
        return distance_matrix

    # Get geographic coordinates for each city
    for city in cities:
        location = get_location(*city)
        city_location_mapping[city] = location

    # Calculate the distance matrix using geographic coordinates
    distance_matrix = get_distance_matrix(city_location_mapping)

    return distance_matrix
