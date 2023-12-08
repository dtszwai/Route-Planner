# Route Planner

This program assists in planning an optimal route for traveling between multiple cities.

You can customize the list of cities in the city.txt file, providing the city name, state name, and country code for each city.

To use this program, you need to obtain an API key from OpenWeatherMap

## Input Cities

The input file [city.txt](city.txt) should have the following format:

```txt
CityName1,StateName1,CountryCode1
CityName2,StateName2,CountryCode2
...
```

Each line represents a city with its associated state and country, separated by commas.

## Example

An example `city.txt` file:

```txt
Vancouver,British Columbia,CA
Oklahoma City,Oklahoma,US
Kansas City,Missouri,US
Riverton,Utah,US
Denver,Colorado,US
New York,New York,US
```

After running the program, the output might be:

```txt
Travel Route:
Vancouver -> Riverton -> Denver -> Kansas City -> Oklahoma City -> New York
```

Feel free to customize the program based on your specific implementation.
