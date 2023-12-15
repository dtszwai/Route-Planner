import json

from algorithm import knn


def get_map_url(cities):
    url = "https://www.google.com/maps/dir/"
    for city in cities:
        city_name = city[0].replace(" ", "+")
        state = city[1].replace(" ", "+")
        country = city[2].replace(" ", "+")
        params = f"{city_name},{state},{country}/"
        url += params
    return url


def main():
    cities_info = [
        tuple(line.strip().split(",")) for line in open("./example/city.txt", "r")
    ]
    distance_matrix = json.load(open("./example/distance_matrix.json", "r"))

    path_order, total_distance = knn(distance_matrix)
    ordered_cities_info = [cities_info[i] for i in path_order]

    route = [city[0] for city in ordered_cities_info]
    formatted_route = " -> ".join(route)

    url = get_map_url(ordered_cities_info)

    # Vancouver -> Riverton -> Denver -> Kansas City -> Oklahoma City -> New York
    print(formatted_route)
    # 6290.5599999999995 km
    print(total_distance, "km")
    # https://www.google.com/maps/dir/Vancouver,British+Columbia,CA/Riverton,Wyoming,US/Denver,Colorado,US/Kansas+City,Missouri,US/Oklahoma+City,Oklahoma,US/New+York,New+York,+US/
    print(url)


if __name__ == "__main__":
    main()
