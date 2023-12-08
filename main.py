import requests
from geopy.distance import geodesic
from dijkstra import dijkstra

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
                distance_matrix[i][j] = 1
            else:
                city1_location = cities_location[cities[i]]
                city2_location = cities_location[cities[j]]

                # Set distance to infinity if it's Vancouver to New York or vice versa
                if (cities[i] == "Vancouver" and cities[j] == "New York") or (
                    cities[i] == "New York" and cities[j] == "Vancouver"
                ):
                    distance_matrix[i][j] = float("inf")
                else:
                    distance_matrix[i][j] = int(
                        geodesic(city1_location, city2_location).km
                    )

    return distance_matrix


if __name__ == "__main__":
    city_location_mapping = {}

    with open("city.txt", "r") as file:
        for line in file:
            city, state, country = line.strip().split(",")

            location = get_location(city=city, state=state, country=country)
            city_location_mapping[city] = location

    distance_matrix = get_distance_matrix(city_location_mapping)

    path = dijkstra(distance_matrix)

    cities = list(city_location_mapping.keys())

    route = [cities[city] for city in path]

    print("Travel Route: ")
    print(" -> ".join(route))
