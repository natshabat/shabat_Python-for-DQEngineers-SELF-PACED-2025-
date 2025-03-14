import sqlite3
import math

# Define radius of the Earth in kilometers
EARTH_RADIUS = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth using the haversine formula.
    Inputs:
      lat1, lon1: Latitude and Longitude of the first city (in degrees)
      lat2, lon2: Latitude and Longitude of the second city (in degrees)
    Output:
      Distance between the two points in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c

    return distance


class CityDistanceCalculator:
    def __init__(self, db_name="city_coordinates.db"):
        """
        Initialize the calculator with an SQLite database for storing city coordinates.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """
        Create a table for storing city coordinates, if it doesn't already exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                city_name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        ''')
        self.connection.commit()

    def get_city_coordinates(self, city_name):
        """
        Fetch coordinates of a city from the database.
        If not found, prompt the user to input the coordinates and save them.
        """
        self.cursor.execute("SELECT latitude, longitude FROM cities WHERE city_name = ?", (city_name,))
        result = self.cursor.fetchone()

        if result:
            return result
        else:
            print(f"Coordinates for '{city_name}' not found in database.")
            latitude = float(input(f"Enter latitude for '{city_name}': "))
            longitude = float(input(f"Enter longitude for '{city_name}': "))
            self.add_city_coordinates(city_name, latitude, longitude)
            return latitude, longitude

    def add_city_coordinates(self, city_name, latitude, longitude):
        """
        Add a city's coordinates to the database.
        """
        self.cursor.execute("INSERT OR REPLACE INTO cities (city_name, latitude, longitude) VALUES (?, ?, ?)",
                            (city_name, latitude, longitude))
        self.connection.commit()

    def calculate_distance(self, city1, city2):
        """
        Calculate the straight-line distance between two cities.
        """
        lat1, lon1 = self.get_city_coordinates(city1)
        lat2, lon2 = self.get_city_coordinates(city2)

        return haversine(lat1, lon1, lat2, lon2)

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()


def main():
    print("Welcome to the City Distance Calculator Tool!")
    calculator = CityDistanceCalculator()

    try:
        while True:
            # Accept two city names from the user
            city1 = input("Enter the first city name (or type 'exit' to quit): ").strip()
            if city1.lower() == 'exit':
                break
            city2 = input("Enter the second city name: ").strip()

            # Calculate the distance between the cities
            distance = calculator.calculate_distance(city1, city2)
            print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} kilometers.\n")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        calculator.close()


if __name__ == "__main__":
    main()