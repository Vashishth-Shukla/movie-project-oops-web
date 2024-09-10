import os

from colorama import Fore, init
from rapidfuzz import fuzz, process  # pip install rapidfuzz

from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


class MovieApp:
    def __init__(self, storage) -> None:
        pass

    @classmethod
    def confirm_use_existing_file(cls, file_name):
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
    def file_exists(cls, file_name):
        if os.path.exists(os.path.join("data", file_name)):
            print(f"The file {file_name} exists.")
            file_name = MovieApp.confirm_use_existing_file(file_name)
            return file_name

    @classmethod
    def get_file_name(cls):
        while True:
            file_name = input("Please enter a file name ending with .csv or .json:")
            if file_name.endswith((".csv", ".json")):
                file_name = MovieApp.file_exists(file_name)
                return file_name
            else:
                print("ERROR: Please enter a name ending with .csv or .json!")

    @classmethod
    def verify_file_name(cls, file_name):
        if file_name.endswith(".csv") or file_name.endswith(".json"):
            file_name = MovieApp.confirm_use_existing_file(file_name)
            return file_name
        else:
            print("Only csv and json files are supported.")
            file_name = MovieApp.get_file_name()

    @classmethod
    def print_title(cls, msg):
        """Print the title of the application."""
        str_num = (78 - len(msg)) // 2 if len(msg) < 78 else 0
        print(f'\n{Fore.CYAN + "*" * str_num} {msg} { "*" * str_num}\n')
