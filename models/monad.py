from collections.abc import Callable
from redis.exceptions import ConnectionError

class RedisMaybeMonad:
    def __init__(self, *data, error_status=None):
        self.data = data
        self.error_status = error_status

    def has_errors(self):
        return self.error_status is not None

    def get_param_at(self, position):
        return self.data[position]

    def bind(self, function: Callable):
        """
        Calls a function with self.data as the parameter and returns a new instance of RepositoryMaybeMonad where self.data stays the same value. 
        Meant to be used with void functions
        """
        print(function.__name__, f"Data: {self.data}, Error Status: {self.error_status}")
        # If Tuple contains None
        if not all(self.data):
            if self.error_status is None:
                return RedisMaybeMonad(None, error_status={"status": 404, "reason": "No data in repository monad"})
            return RedisMaybeMonad(None, error_status=self.error_status)
        try:
            function(*self.data)
            return RedisMaybeMonad(*self.data, error_status=self.error_status)
        except ConnectionError:
            return RedisMaybeMonad(None, error_status={"status": 502, "reason": "Failed to connect to Redis"})
        


    def bind_data(self, function: Callable):
        """
        Calls a function with self.data as the parameter and returns a new instance of RepositoryMaybeMonad with self.data as the result of the function 
        Meant to be used with function that has a return value
        """
        print(function.__name__, f"Data: {self.data}, Error Status: {self.error_status}")
        # If Tuple contains None
        if not all(self.data):
            if self.error_status is None:
                return RedisMaybeMonad(None, error_status={"status": 404, "reason": "No data in repository monad"})
            return RedisMaybeMonad(None, error_status=self.error_status)
        try:
            result = function(*self.data)
            return RedisMaybeMonad(result, error_status=self.error_status)
        except ConnectionError:
            return RedisMaybeMonad(None, error_status={"status": 502, "reason": "Failed to connect to Redis"})