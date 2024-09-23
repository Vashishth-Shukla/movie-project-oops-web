import os
import random
import sys

import requests
from colorama import Fore, init
from dotenv import load_dotenv
from rapidfuzz import fuzz, process

init(autoreset=True)
load_dotenv("backend/.env")


class MovieApp:
    INDEX_TEMPLATE_PATH = "templates/index_template.html"
    MOVIE_TEMPLATE_PATH = "templates/movie_li.html"
    URI = r"http://www.omdbapi.com/?"

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
        "Create Website",
    ]

    def __init__(self, storage) -> None:
        """
        Initialize the MovieApp with a storage object.

        Args:
            storage (object): An object that handles storing and retrieving movie data.
        """
        self.storage = storage

    def _get_movie_poster_manually(self) -> str:
        """
        Prompt the user to manually enter a URL for the movie poster.

        Returns:
            str: The URL of the movie poster entered by the user.
        """
        return input(Fore.YELLOW + "Please enter a valid URL to the movie poster: ")

    def _get_movie_details(self, movie_name: str) -> tuple:
        """
        Fetch movie details from the OMDB API or manually from the user if API fails.

        Args:
            movie_name (str): The name of the movie to get details for.

        Returns:
            tuple: A tuple containing the movie name, year, rating, and poster URL.
        """
        movie_details = {}

        try:
            request_uri = MovieApp.URI + os.getenv("API_KEY") + f"&t={movie_name}"
            movie_details = requests.get(request_uri).json()
            if movie_details["Response"]:
                movie_name = movie_details["Title"]
                year = movie_details["Year"]
                rating = movie_details["imdbRating"]
                poster = movie_details["Poster"]
            else:
                print(Fore.RED + "Movie details not found!")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            print(Fore.YELLOW + "We will get the details manually.")
            year = self._get_movie_year_manually(movie_name)
            rating = self._get_movie_rating_manually()
            poster = self._get_movie_poster_manually()

        return movie_name, year, rating, poster

    def _get_movie_rating_manually(self) -> float:
        """
        Prompt the user to enter a rating for the movie.

        Returns:
            float: The movie rating entered by the user.
        """
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

    def _get_movie_year_manually(self, movie_name) -> int:
        """
        Prompt the user to enter the release year of the movie.

        Returns:
            int: The year of the movie entered by the user.
        """
        while True:
            year = input(Fore.YELLOW + f"Enter release year for '{movie_name}': ")
            try:
                year = int(year)
                print(Fore.GREEN + f"Valid year entered: {year}")
                return year
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a valid year.")

    def _add_movie(self) -> None:
        """
        Add a new movie to the database by prompting the user for movie details.
        """
        movie_name = input(Fore.YELLOW + "Enter new movie name: ")
        movie_name, year, rating, poster = self._get_movie_details(movie_name)
        self.storage.add_movie(movie_name, year, rating, poster)
        print(Fore.GREEN + f"{movie_name} added.")

    def _delete_movie(self) -> None:
        """
        Delete a movie from the database by prompting the user for the movie name.
        """
        movie = input(Fore.YELLOW + "Enter the movie name to delete: ")
        self.storage.delete_movie(movie)
        print(Fore.GREEN + f"{movie} deleted.")

    def _update_movie(self) -> None:
        """
        Update the rating of an existing movie in the database.
        """
        movie = input(Fore.YELLOW + "Enter the movie to update: ")
        new_rating = self._get_movie_rating_manually()
        self.storage.update_movie(movie, new_rating)
        print(Fore.GREEN + f"Rating for {movie} updated to {new_rating}.")

    def _average_rating(self, movies: dict) -> float:
        """
        Calculate the average rating of all movies in the database.

        Args:
            movies (dict): A dictionary of movies with details.

        Returns:
            float: The average rating of the movies.
        """
        return sum(float(details["rating"]) for details in movies.values()) / len(
            movies
        )

    def _median_rating(self, movies: dict) -> float:
        """
        Calculate the median rating of all movies in the database.

        Args:
            movies (dict): A dictionary of movies with details.

        Returns:
            float: The median rating of the movies.
        """
        ratings = sorted(float(details["rating"]) for details in movies.values())
        n = len(ratings)
        mid = n // 2
        return (ratings[mid] + ratings[-mid - 1]) / 2 if n % 2 == 0 else ratings[mid]

    def _print_best_movies(self, movies: dict) -> None:
        """
        Print the best-rated movie(s) in the database.

        Args:
            movies (dict): A dictionary of movies with details.
        """
        print(Fore.GREEN + "Best Movie(s):")
        max_rating = max(float(details["rating"]) for details in movies.values())
        for movie, details in movies.items():
            if float(details["rating"]) == max_rating:
                print(Fore.GREEN + f"\t{movie}: {details['rating']}")

    def _print_worst_movies(self, movies: dict) -> None:
        """
        Print the worst-rated movie(s) in the database.

        Args:
            movies (dict): A dictionary of movies with details.
        """
        print(Fore.RED + "Worst Movie(s):")
        min_rating = min(float(details["rating"]) for details in movies.values())
        for movie, details in movies.items():
            if float(details["rating"]) == min_rating:
                print(Fore.RED + f"\t{movie}: {details['rating']}")

    def _stats(self) -> None:
        """
        Display statistics about the movie ratings in the database.
        """
        movies = self.storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found to calculate stats.")
            return
        print(Fore.CYAN + f"Average rating: {self._average_rating(movies):.2f}")
        print(Fore.CYAN + f"Median rating: {self._median_rating(movies):.2f}")
        self._print_best_movies(movies)
        self._print_worst_movies(movies)
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _random_movie(self) -> None:
        """
        Suggest a random movie from the database.
        """
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

    def _search_movie(self) -> None:
        """
        Search for a movie in the database and suggest similar movies if not found.
        """
        movie = input(Fore.YELLOW + "Enter the movie name to search: ")
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

    def _sort_by_rating(self) -> None:
        """
        Sort and display movies by their ratings in descending order.
        """
        movies = self.storage.list_movies()
        sorted_movies = sorted(
            movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True
        )
        for movie, details in sorted_movies:
            print(Fore.CYAN + f"{movie}: {details['rating']}")
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _list_movies(self) -> None:
        """
        List all movies from the database.
        """
        movies = self.storage.list_movies()
        if movies:
            print(Fore.CYAN + f"\n{len(movies)} movies in total\n")
            for title, details in movies.items():
                print(Fore.CYAN + f"{title}: {details.get('rating', 'N/A')}")
        else:
            print(Fore.RED + "No movies found.")
        input(Fore.GREEN + "\nPress Enter to continue...")

    def _create_website(self) -> None:
        """
        Generate a static website displaying the movie collection.
        """
        # Step 1: Read the template files
        with open(MovieApp.INDEX_TEMPLATE_PATH, "r") as index_file:
            index_template = index_file.read()

        with open(MovieApp.MOVIE_TEMPLATE_PATH, "r") as movie_li_file:
            movie_li_template = movie_li_file.read()

        # Step 2: Get all movies from storage
        movies = self.storage.list_movies()

        # Step 3: Generate the movie list items
        movie_list_items = ""
        for title, details in movies.items():
            # Replace placeholders in movie_li.html with actual movie details
            movie_li = movie_li_template.replace(
                "--movie-poster-link--", details["poster"]
            )
            movie_li = movie_li.replace("--movie-name--", title)
            movie_li = movie_li.replace("--movie-year--", str(details["year"]))
            movie_list_items += movie_li

        # Step 4: Replace placeholders in index template
        index_content = index_template.replace(
            "__TEMPLATE_TITLE__", "My Movie Collection"
        )
        index_content = index_content.replace(
            "__TEMPLATE_MOVIE_GRID__", movie_list_items
        )

        # Step 5: Write the final HTML content to index.html
        with open("index.html", "w") as output_file:
            output_file.write(index_content)

        print(Fore.GREEN + "Website created successfully!")

    def _function_handler(self, choice: str) -> None:
        """
        Handle the user's menu choice by calling the appropriate method.

        Args:
            choice (str): The user's menu choice as a string.
        """
        if choice == "0":
            MovieApp._exit_app()
        elif choice == "1":
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
        elif choice == "9":
            self._create_website()
        else:
            print(Fore.RED + "\nIncorrect input. Please try again.\n")

    def run(self) -> None:
        """
        Run the application, displaying the menu and handling user choices.
        """
        while True:
            MovieApp._print_menu()
            user_choice = input(Fore.YELLOW + "Enter choice (0-9): ")
            self._function_handler(user_choice)

    @classmethod
    def _print_menu(cls) -> None:
        """
        Print the main menu of the application.
        """
        print(Fore.MAGENTA + "Menu:\n")
        for index, item in enumerate(MovieApp.MAIN_MENU_ITEMS):
            print(Fore.MAGENTA + f"{index}. {item}")

    @classmethod
    def _confirm_use_existing_file(cls, file_name: str) -> str:
        """
        Confirm with the user if they want to use an existing file.

        Args:
            file_name (str): The name of the existing file.

        Returns:
            str: The file name to use, possibly modified based on user input.
        """

        while True:
            selection = input(
                Fore.YELLOW + "Would you like to use the existing file? (y/n): "
            )
            if selection.lower() == "y":
                return file_name
            elif selection.lower() == "n":
                print(Fore.YELLOW + "Please use another name.")
                file_name = MovieApp.get_file_name()
                return file_name
            else:
                print(
                    Fore.RED
                    + "ERROR: Incorrect input. Please enter 'y' for yes and 'n' for no."
                )

    @classmethod
    def _file_exists(cls, file_name: str) -> str:
        """
        Check if the file exists and prompt the user to confirm usage.

        Args:
            file_name (str): The name of the file to check.

        Returns:
            str: The confirmed file name to use.
        """
        if os.path.exists(os.path.join("data", file_name)):
            print(Fore.YELLOW + f"The file {file_name} exists.")
            file_name = MovieApp._confirm_use_existing_file(file_name)
        return file_name

    @classmethod
    def get_file_name(cls) -> str:
        """
        Prompt the user to enter a file name ending with .csv or .json.

        Returns:
            str: The file name entered by the user, validated.
        """
        while True:
            file_name = input(
                Fore.YELLOW + "Please enter a file name ending with .csv or .json: "
            )
            if file_name.endswith((".csv", ".json")):
                file_name = MovieApp._file_exists(file_name)
                return file_name
            else:
                print(
                    Fore.RED + "ERROR: Please enter a name ending with .csv or .json!"
                )

    @classmethod
    def verify_file_name(cls, file_name: str) -> str:
        """
        Verify if the file name ends with .csv or .json, prompting user if necessary.

        Args:
            file_name (str): The initial file name to verify.

        Returns:
            str: The verified file name.
        """
        if file_name.endswith((".csv", ".json")):
            file_name = MovieApp._file_exists(file_name)
            return file_name
        else:
            print(Fore.RED + "Only csv and json files are supported.")
            file_name = MovieApp.get_file_name()
            return file_name

    @classmethod
    def _print_title(cls, msg: str) -> None:
        """
        Print the title of the application.

        Args:
            msg (str): The message to display as the title.
        """
        str_num = (78 - len(msg)) // 2 if len(msg) < 78 else 0
        print(Fore.CYAN + f'\n{"*" * str_num} {msg} {"*" * str_num}\n')

    @classmethod
    def _exit_app(cls) -> None:
        """
        Exit the application.
        """
        print(Fore.CYAN + "\nExiting the application\n")
        sys.exit()
