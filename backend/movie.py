import random
import sys

from colorama import Fore, init
from rapidfuzz import fuzz, process  # pip install rapidfuzz

# Initialize colorama
init(autoreset=True)

# Constants
MAIN_MENU_ITEMS = [
    "List movies",
    "Add movie",
    "Delete movie",
    "Update movie",
    "Stats",
    "Random movie",
    "Search movie",
    "Movies sorted by rating",
]

# Dictionary to store the movies and the rating
MOVIES = {
    "The Shawshank Redemption": 9.5,
    "Pulp Fiction": 8.8,
    "The Room": 3.6,
    "The Godfather": 9.2,
    "The Godfather: Part II": 9.0,
    "The Dark Knight": 9.0,
    "12 Angry Men": 8.9,
    "Everything Everywhere All At Once": 8.9,
    "Forrest Gump": 8.8,
    "Star Wars: Episode V": 8.7,
}


def print_title():
    """Print the title of the application."""
    print(f'\n{Fore.CYAN + "*" * 10} My Movies Database { "*" * 10}\n')


def print_menu():
    """Print the main menu."""
    print(Fore.MAGENTA + "Menu:\n")
    for i in range(len(MAIN_MENU_ITEMS)):
        print(Fore.MAGENTA + f"{i + 1}. {MAIN_MENU_ITEMS[i]}")
    print(Fore.MAGENTA + "\nE. Exit My Movies Database")


def list_movies():
    """List all the movies with their ratings."""
    print(f"\n{len(MOVIES)} movies in total\n")
    for k, v in MOVIES.items():
        print(f"{k}: {v}")
    input(Fore.GREEN + "\nPress Enter to continue...")


def _get_movie_rating():
    """Get a valid movie rating from the user."""
    while True:
        try:
            rating = float(input(Fore.YELLOW + "Enter new movie rating (0-10): "))
            if 0 <= rating <= 10:
                return rating
            else:
                print(Fore.RED + "Rating must be between 0 and 10. Please try again.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 0 and 10.")


def add_movie():
    """Add a new movie to the database."""
    movie_name = input(Fore.YELLOW + "Enter new movie name: ")
    rating = _get_movie_rating()
    MOVIES[movie_name] = rating
    print(f"{movie_name}: {rating} added to the movies list.")
    input(Fore.GREEN + "\nPress Enter to continue...")


def delete_movie():
    """Delete a movie from the database."""
    movie = input(Fore.YELLOW + "\nEnter the movie name to delete: ")

    if movie in MOVIES.keys():
        MOVIES.pop(movie)
        print(Fore.GREEN + f"{movie} deleted successfully.")
    else:
        print(Fore.RED + f"{movie} not in the movie list.")

    input(Fore.GREEN + "\nPress Enter to continue...")


def update_movie():
    """Update the rating of an existing movie."""
    movie = input(Fore.YELLOW + "\nEnter the movie to update: ")

    if movie in MOVIES.keys():
        new_rating = _get_movie_rating()
        MOVIES[movie] = new_rating
        print(
            Fore.GREEN + f"The movie {movie} has been updated to rating {new_rating}."
        )
    else:
        print(Fore.RED + f"The movie {movie} is not in the movie list.")

    input(Fore.GREEN + "\nPress Enter to continue...")


def _average_rating():
    """Calculate the average rating of all movies."""
    return sum(MOVIES.values()) / len(MOVIES)


def _median_rating():
    """Calculate the median rating of all movies."""
    ratings = sorted(MOVIES.values())
    n = len(ratings)
    mid = n // 2
    return (ratings[mid] + ratings[-mid - 1]) / 2 if n % 2 == 0 else ratings[mid]


def _print_best_movies():
    """Print the best-rated movie(s)."""
    print("Best Movie: ")
    max_rating = max(MOVIES.values())
    for movie, rating in MOVIES.items():
        if rating == max_rating:
            print(f"\t{movie}: {rating}")


def _print_worst_movies():
    """Print the worst-rated movie(s)."""
    print("Worst Movie: ")
    min_rating = min(MOVIES.values())
    for movie, rating in MOVIES.items():
        if rating == min_rating:
            print(f"\t{movie}: {rating}")


def stats():
    """Print statistics of the movie ratings."""
    print(f"Average rating: {_average_rating():.2f}")
    print(f"Median rating: {_median_rating()}")
    _print_best_movies()
    _print_worst_movies()
    input(Fore.GREEN + "\nPress Enter to continue...")


def random_movie():
    """Suggest a random movie."""
    movie = random.choice(list(MOVIES.keys()))
    print(f"Your tonight's movie is {movie} with rating {MOVIES[movie]}")
    input(Fore.GREEN + "\nPress Enter to continue...")


def search_movie():
    """Search for a movie and suggest similar movies if not found."""
    movie = input(Fore.YELLOW + "\nEnter the movie name to search: ")

    if movie in MOVIES.keys():
        print(f"The movie {movie} has a rating of {MOVIES[movie]}")
    else:
        similar_movies = process.extract(
            movie, MOVIES.keys(), limit=3, scorer=fuzz.ratio
        )

        if similar_movies:
            print(Fore.RED + f"The movie '{movie}' does not exist. Did you mean:")
            for similar_movie, score, _ in similar_movies:
                print(Fore.YELLOW + f"- {similar_movie} (similarity: {score}%)")
        else:
            print(Fore.RED + f"No similar movies found for '{movie}'.")

    input(Fore.GREEN + "\nPress Enter to continue...")


def sort_by_rating():
    """Sort and display movies by their ratings."""
    sorted_movies = sorted(MOVIES.items(), key=lambda x: x[1], reverse=True)
    for movie, rating in sorted_movies:
        print(f"{movie}: {rating}")

    input(Fore.GREEN + "\nPress Enter to continue...")


def exit_app():
    """Exit the application."""
    print(Fore.CYAN + "\nExiting the application\n")
    sys.exit()


def function_handler(choice):
    """Handle the user's menu choice."""
    if choice == "1":
        list_movies()
    elif choice == "2":
        add_movie()
    elif choice == "3":
        delete_movie()
    elif choice == "4":
        update_movie()
    elif choice == "5":
        stats()
    elif choice == "6":
        random_movie()
    elif choice == "7":
        search_movie()
    elif choice == "8":
        sort_by_rating()
    elif choice == "E":
        exit_app()
    else:
        print(Fore.RED + "\nIncorrect input. Please try again\n")


def main():
    """Main function to run the application."""
    print_title()
    while True:
        print_menu()
        user_choice = input("\nEnter choice (1-8 or E): ")
        function_handler(user_choice)


if __name__ == "__main__":
    main()
