# Route Planner

This program assists in planning an optimal route for traveling between multiple cities.

You can customize the list of cities in the `city.txt` file, providing the city name, state name, and country code for each city.

To use this program, you need to obtain an API key from OpenWeatherMap

## Setup

Install the required dependencies by running:

```bash
pip3 install -r requirements.txt
```

Create a .env file in the project directory and add the following lines, replacing <YOUR_GOOGLE_MAP_API_KEY> and <YOUR_OPEN_WEATHER_MAP_API_KEY> with your actual API keys.

```txt
GOOGLE_MAP_API_KEY="<YOUR_GOOGLE_MAP_API_KEY>"
OPEN_WEATHER_MAP_API_KEY="<YOUR_OPEN_WEATHER_MAP_API_KEY>"
```

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
Riverton,Wyoming,US
Denver,Colorado,US
New York,New York, US
```

## Running the Program

To run the program, use the following command:

```bash
streamlit run main.py [city_file_path] [data_source] (optional)
```

For example:

```bash
# Using Google Maps as a Data Source:
streamlit run main.py city.txt google_maps

# Using Coordinates to Calculate Distances:
streamlit run main.py city.txt coordinate

# Default case (city.txt and Google Maps)
streamlit run main.py
```

If the `data_source` is set to `google_maps`, the program will use Google Maps data to calculate the distance between cities.

If the `data_source` is set to `coordinate`, the program will calculate the distance between cities using coordinates.
