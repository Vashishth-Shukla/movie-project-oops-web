import csv
import os

from storage.istorage import IStorage


class StorageCsv(IStorage):

    def __init__(self, file_name):
        _data = "data"  # Relative path to the "data" directory
        self._file_path = os.path.join(_data, file_name)

    def _read_data(self):
        """Reads the existing movie data from the CSV file."""
        movies = {}
        try:
            with open(self._file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "year": int(row["year"]),
                        "rating": float(row["rating"]),
                        "poster": row["poster"],  # Optional field, can be empty
                    }
        except FileNotFoundError:
            movies = {}  # Initialize with an empty dictionary if file not found
        return movies

    def _write_data(self, movies):
        """Writes the movie data to the CSV file."""
        with open(self._file_path, mode="w", newline="") as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow(
                    {
                        "title": title,
                        "year": details["year"],
                        "rating": details["rating"],
                        "poster": details.get("poster", ""),
                    }
                )

    def list_movies(self):
        """Returns the list of movies."""
        movies = self._read_data()
        return movies

    def add_movie(self, title, year, rating, poster=None):
        """Adds a new movie to the CSV file."""
        movies = self._read_data()
        if title in movies:
            print(f"Movie '{title}' already exists in the database.")
            return

        # Add new movie details
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,  # Optional field for poster
        }

        self._write_data(movies)
        print(f"Movie '{title}' added successfully.")

    def delete_movie(self, title):
        """Deletes a movie by title from the CSV file."""
        movies = self._read_data()
        if title.lower() in (key.lower() for key in movies.keys()):
            lowercase_movies = {key.lower(): key for key in movies}
            title_in_db = lowercase_movies.get(title.lower())
            del movies[title_in_db]
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found in the database.")

    def update_movie(self, title, rating):
        """Updates the rating of an existing movie."""
        movies = self._read_data()
        if title.lower() in [movie.lower() for movie in movies.keys()]:
            lowercase_movies = {key.lower(): key for key in movies}
            matched_title = lowercase_movies.get(title.lower())
            movies[matched_title]["rating"] = rating
            self._write_data(movies)
            print(f"Movie '{matched_title}' rating updated to {rating}.")
        else:
            print(f"Movie '{title}' not found in the database.")


# Sanity check


def main():
    storage = StorageCsv("test.csv")

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
