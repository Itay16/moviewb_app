from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_movie_data):
        pass
