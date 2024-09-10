import json
import os

from storage.istorage import IStorage


class StorageJson(IStorage):

    def __init__(self, file_name):
        _data = "data"  # Relative path to the "data" directory
        self._file_path = os.path.join(_data, file_name)

    def _read_data(self):
        """Reads the existing movie data from the file."""
        try:
            with open(self._file_path, "r") as file:
                movies = lambda: json.load(file) if json.load(file) is not None else {}
        except FileNotFoundError:
            movies = {}  # Initialize with an empty dictionary if file not found
        return movies

    def _write_data(self, movies):
        """Writes the movie data to the file."""
        with open(self._file_path, "w") as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """Returns the list of movies."""
        movies = self._read_data()
        return movies

    def add_movie(self, title, year, rating, poster=None):
        """Adds a new movie to the JSON file."""
        movies = self._read_data()  # Read the current movies data
        if title in movies:
            print(f"Movie '{title}' already exists in the database.")
            return  # no further actions required
        else:
            # Add new movie details
            movies[title] = {"year": year, "rating": rating, "poster": poster}

        self._write_data(movies)  # Write updated movies data back to the file
        print(f"Movie '{title}' added successfully.")

    def delete_movie(self, title):
        """Deletes a movie by title from the JSON file."""
        movies = self._read_data()
        if title in movies:
            del movies[title]
            self._write_data(movies)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found in the database.")

    def update_movie(self, title, rating):
        """Updates the rating of an existing movie."""
        movies = self._read_data()
        if title in movies:
            movies[title]["rating"] = rating
            self._write_data(movies)
            print(f"Movie '{title}' rating updated to {rating}.")
        else:
            print(f"Movie '{title}' not found in the database.")


# Sanity check


def main():
    storage = StorageJson("test.json")

    # List existing movies
    print("Current movies in the database:")
    print(storage.list_movies())

    # Add a new movie
    storage.add_movie("Inception", 2010, 8.8)

    # Update a movie's rating
    storage.update_movie("Inception", 9.0)

    # Delete a movie
    storage.delete_movie("Titanic")

    # List updated movies
    print("Updated movies in the database:")
    print(storage.list_movies())


if __name__ == "__main__":
    main()
