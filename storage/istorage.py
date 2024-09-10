from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """Return the strings to print the movies in a storage."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Add the movie with given input to the storage."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Delete given movie from the storage."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Update the movie ratings for the given movie."""
        pass
