import json
import os

POST_FILE = "data/posts.json"
REACTION_FILE = "data/reactions.json"
USER_FILE = "data/users.json"


class DataManager:
    """Centralized data management"""
    
    @staticmethod
    def load(file: str) -> dict:
        if os.path.exists(file):
            with open(file) as f:
                return json.load(f)
        return {}

    @staticmethod
    def save(file: str, data: dict) -> None:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def get_users(cls) -> dict:
        return cls.load(USER_FILE)

    @classmethod
    def get_posts(cls) -> dict:
        return cls.load(POST_FILE)

    @classmethod
    def get_reactions(cls) -> dict:
        return cls.load(REACTION_FILE)