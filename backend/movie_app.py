import os
import random
import sys

from colorama import Fore, init
from rapidfuzz import fuzz, process  # pip install rapidfuzz

from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson

init(autoreset=True)


class MovieApp:

    MAIN_MENU_ITEMS = [
        "Exit My Movies Database",
        "List movies",
        "Add movie",
        "Delete movie",
        "Update movie",
        "Stats",
        "Random movie",
        "Search movie",
        "Movies sorted by rating",
    ]

    def __init__(self, storage) -> None:
        self.storage = storage

    def _get_movie_rating(self):
        """Get a valid movie rating from the user."""
        while True:
            try:
                rating = float(input(Fore.YELLOW + "Enter movie rating (0-10): "))
                if 0 <= rating <= 10:
                    return rating
                else:
                    print(
                        Fore.RED + "Rating must be between 0 and 10. Please try again."
                    )
            except ValueError:
                print(
                    Fore.RED + "Invalid input. Please enter a number between 0 and 10."
                )

    def _add_movie(self):
        """Add a new movie to the database."""
        movie_name = input(Fore.YELLOW + "Enter new movie name: ")
        year = input(Fore.YELLOW + "Enter movie release year: ")
        rating = self._get_movie_rating()
        poster = input(Fore.YELLOW + "Enter poster URL (optional): ")
        self.storage.add_movie(movie_name, year, rating, poster)

    def _delete_movie(self):
        """Delete a movie from the database."""
        movie = input(Fore.YELLOW + "\nEnter the movie name to delete: ")
        self.storage.delete_movie(movie)

    def _update_movie(self):
        """Update the rating of an existing movie."""
        movie = input(Fore.YELLOW + "\nEnter the movie to update: ")
        new_rating = self._get_movie_rating()
        self.storage.update_movie(movie, new_rating)

    def _average_rating(self, movies):
        """Calculate the average rating of all movies."""
        return sum(float(details["rating"]) for details in movies.values()) / len(
            movies
        )

    def _median_rating(self, movies):
        """Calculate the median rating of all movies."""
        ratings = sorted(float(details["rating"]) for details in movies.values())
        n = len(ratings)
        mid = n // 2
        return (ratings[mid] + ratings[-mid - 1]) / 2 if n % 2 == 0 else ratings[mid]

    def _print_best_movies(self, movies):
        """Print the best-rated movie(s)."""
        print(Fore.GREEN + "Best Movie(s):")
        max_rating = max(float(details["rating"]) for details in movies.values())
        for movie, details in movies.items():
            if float(details["rating"]) == max_rating:
                print(Fore.GREEN + f"\t{movie}: {details['rating']}")

    def _print_worst_movies(self, movies):
        """Print the worst-rated movie(s)."""
        print(Fore.RED + "Worst Movie(s):")
        min_rating = min(float(details["rating"]) for details in movies.values())
        for movie, details in movies.items():
            if float(details["rating"]) == min_rating:
                print(Fore.RED + f"\t{movie}: {details['rating']}")

    def _stats(self):
        """Display statistics about the movie ratings."""
        movies = self.storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found to calculate stats.")
            return
        print(Fore.CYAN + f"Average rating: {self._average_rating(movies):.2f}")
        print(Fore.CYAN + f"Median rating: {self._median_rating(movies):.2f}")
        self._print_best_movies(movies)
        self._print_worst_movies(movies)
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _random_movie(self):
        """Suggest a random movie."""
        movies = list(self.storage.list_movies().keys())
        if not movies:
            print(Fore.RED + "No movies found to suggest.")
            return
        movie = random.choice(movies)
        rating = self.storage.list_movies()[movie]["rating"]
        print(
            Fore.CYAN
            + f"Your movie suggestion for tonight is '{movie}' with a rating of {rating}."
        )
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _search_movie(self):
        """Search for a movie and suggest similar movies if not found."""
        movie = input(Fore.YELLOW + "\nEnter the movie name to search: ")
        movies = self.storage.list_movies()
        if movie in movies:
            print(
                Fore.GREEN
                + f"The movie '{movie}' has a rating of {movies[movie]['rating']}."
            )
        else:
            similar_movies = process.extract(
                movie, movies.keys(), limit=3, scorer=fuzz.ratio
            )
            if similar_movies:
                print(Fore.RED + f"The movie '{movie}' does not exist. Did you mean:")
                for similar_movie, score, _ in similar_movies:
                    print(Fore.YELLOW + f"- {similar_movie} (similarity: {score}%)")
            else:
                print(Fore.RED + f"No similar movies found for '{movie}'.")
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _sort_by_rating(self):
        """Sort and display movies by their ratings."""
        movies = self.storage.list_movies()
        sorted_movies = sorted(
            movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True
        )
        for movie, details in sorted_movies:
            print(Fore.CYAN + f"{movie}: {details['rating']}")
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _list_movies(self):
        """List all movies from storage."""
        movies = self.storage.list_movies()
        if movies:
            print(Fore.CYAN + f"\n{len(movies)} movies in total\n")
            for title, details in movies.items():
                print(Fore.CYAN + f"{title}: {details.get('rating', 'N/A')}")
        else:
            print(Fore.RED + "No movies found.")
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _function_handler(self, choice):
        """Handle the user's menu choice."""
        if choice == "0":
            MovieApp._exit_app()
        if choice == "1":
            self._list_movies()
        elif choice == "2":
            self._add_movie()
        elif choice == "3":
            self._delete_movie()
        elif choice == "4":
            self._update_movie()
        elif choice == "5":
            self._stats()
        elif choice == "6":
            self._random_movie()
        elif choice == "7":
            self._search_movie()
        elif choice == "8":
            self._sort_by_rating()
        else:
            print(Fore.RED + "\nIncorrect input. Please try again\n")

    def run(self):
        while True:
            MovieApp._print_menu()
            user_choice = input("\nEnter choice (0-8): ")
            self._function_handler(user_choice)

    @classmethod
    def _print_menu(cls):
        """Print the main menu."""
        print(Fore.MAGENTA + "Menu:\n")
        for index, item in enumerate(MovieApp.MAIN_MENU_ITEMS):
            print(Fore.MAGENTA + f"{index}. {item}")

    @classmethod
    def _confirm_use_existing_file(cls, file_name):
        while True:
            selection = input("Would you like to use the existing file? (y/n):")
            if selection.lower() == "y":
                return file_name
            elif selection.lower() == "n":
                print("Plese use another name.")
                file_name = MovieApp.get_file_name()
                return file_name
            else:
                print(
                    "ERROR: Incorrect input.\n \
                    Please enter 'y' for yes and 'n' for no."
                )

    @classmethod
    def _file_exists(cls, file_name):
        if os.path.exists(os.path.join("data", file_name)):
            print(f"The file {file_name} exists.")
            file_name = MovieApp._confirm_use_existing_file(file_name)
            return file_name

    @classmethod
    def get_file_name(cls):
        while True:
            file_name = input("Please enter a file name ending with .csv or .json:")
            if file_name.endswith((".csv", ".json")):
                file_name = MovieApp._file_exists(file_name)
                return file_name
            else:
                print("ERROR: Please enter a name ending with .csv or .json!")

    @classmethod
    def verify_file_name(cls, file_name):
        if file_name.endswith(".csv") or file_name.endswith(".json"):
            file_name = MovieApp._confirm_use_existing_file(file_name)
            return file_name
        else:
            print("Only csv and json files are supported.")
            file_name = MovieApp.get_file_name()

    @classmethod
    def _print_title(cls, msg):
        """Print the title of the application."""
        str_num = (78 - len(msg)) // 2 if len(msg) < 78 else 0
        print(f'\n{Fore.CYAN + "*" * str_num} {msg} { "*" * str_num}\n')

    @classmethod
    def _exit_app(cls):
        """Exit the application."""
        print(Fore.CYAN + "\nExiting the application\n")
        sys.exit()
