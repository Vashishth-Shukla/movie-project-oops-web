import argparse

from backend.movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Enter the filename of the database you wish to access.\n \
        The format of the input shuld be 'name.format'. \n \
        Exmaple: python3 main.py -f abc.json"
    )

    # Add an optional argument for the filename
    parser.add_argument("-f", "--file", type=str, help="Database file", default=None)

    # Parse the arguments
    args = parser.parse_args()

    MovieApp._print_title("Welcome to the movie database")

    # Check if the filename is provided
    if args.file:
        file_name = MovieApp.verify_file_name(args.file)
    else:
        file_name = MovieApp.get_file_name()

    storage = (
        StorageCsv(file_name) if file_name.endswith(".csv") else StorageJson(file_name)
    )
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
