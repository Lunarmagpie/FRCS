from contextlib import suppress
from os import environ
from dotenv import dotenv_values


class EnvironmentVariableNotFoundError(Exception):
    """Raised when an environment variable can't be loaded"""


class Environment:
    def __init__(self):
        self.env = dotenv_values(".env")

    def __getitem__(self, key: str) -> str:
        with suppress(KeyError):
            return environ[key]
        with suppress(KeyError):
            return self.env[key]

        raise EnvironmentVariableNotFoundError(
            f"Environment variable `{key}` not found in .env file or sytem environment"
            "variables."
        )

env = Environment()
