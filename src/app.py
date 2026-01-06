import random
from datetime import datetime
from functools import wraps
from typing import Optional

from .models.user import User
from .services.data_manager import DataManager
from .services.reaction_manager import ReactionManager
from .services.analytics_engine import AnalyticsEngine


# -------------------- DECORATORS --------------------
def require_login(func):
    """Decorator to ensure user is logged in"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            print("✗ Please login first!")
            return None
        return func(self, *args, **kwargs)
    return wrapper


class SocialMediaApp:
    def __init__(self):
        self.current_user: Optional[User] = None
        self._init_files()
        self._setup_menus()

    def _init_files(self) -> None:
        """Initialize all necessary files"""
        if not DataManager.load("data/users.json"):
            DataManager.save("data/users.json", {
                "admin": {
                    "user_id": 0, "username": "admin", "name": "Admin User",
                    "email": "admin@example.com",
                    "skills": ["Management", "Moderation", "Support", "Communication", "Leadership"]
                }
            })

        if not DataManager.load("data/posts.json"):
            posts = {
                str(i): {"username": "admin", "content": f"Sample Post {i}", "time": str(datetime.now())}
                for i in range(1, 11)
            }
            DataManager.save("data/posts.json", posts)

        if not DataManager.load("data/reactions.json"):
            DataManager.save("data/reactions.json", {})

    def _setup_menus(self) -> None:
        """Setup menu configurations"""
        self.guest_menu = {
            "1": ("Create Profile", self.create_profile),
            "2": ("Login", self.login),
            "3": ("Exit", lambda: exit("Goodbye!"))
        }

        self.user_menu = {
            "1": ("View Profile", self.view_profile),
            "2": ("Edit Profile", self.edit_profile),
            "3": ("Create Post", self.create_post),
            "4": ("React to Post", self.react_to_post),
            "5": ("Show Post Details", self.show_post_details),
            "6": ("My Analytics", self.analytics),
            "7": ("Logout", self.logout),
            "8": ("Exit", lambda: exit("Goodbye!"))
        }

    def _validate_user(self, username: str) -> bool:
        return username in DataManager.get_users()

    def _get_input(self, prompt: str, validator=None) -> str:
        while True:
            value = input(prompt).strip()
            if value == "back":
                return "back"
            if not validator or validator(value):
                return value
            print("✗ Invalid input. Please try again or 'back' to cancel.")

    def create_profile(self) -> None:
        print("\n--- Create Profile ---")
        while True:
            username = input("Username (or 'back' to cancel): ").strip()
            if username == "back":
                return
            if username and not self._validate_user(username):
                break
            print("✗ Username exists or empty! Please try again or 'back' to cancel.")
        
        name = input("Name: ")
        email = input("Email: ")
        skills = [input(f"Skill {i+1}: ") for i in range(5)]

        user = User(username, name, email, skills)
        users = DataManager.get_users()
        users[username] = user.to_dict()
        DataManager.save("data/users.json", users)

        self.current_user = user
        print(f"✓ Profile Created Successfully! Welcome, {username}!")

    def login(self) -> None:
        print("\n--- Login ---")
        username = input("Username (or 'back' to cancel): ").strip()
        if username == "back":
            return

        if not self._validate_user(username):
            print("✗ User not found! Please create a profile first.")
            return

        self.current_user = User.from_dict(DataManager.get_users()[username])
        print(f"✓ Welcome back, {username}!")

    @require_login
    def edit_profile(self) -> None:
        self.current_user.edit_profile()
        users = DataManager.get_users()
        users[self.current_user.username] = self.current_user.to_dict()
        DataManager.save("data/users.json", users)
        print("✓ Profile updated successfully!")

    @require_login
    def create_post(self) -> None:
        posts = DataManager.get_posts()
        pid = str(len(posts) + 1)
        content = input("\nWrite your post: ")

        posts[pid] = {
            "username": self.current_user.username,
            "content": content,
            "time": str(datetime.now())
        }
        DataManager.save("data/posts.json", posts)
        print("✓ Post Created Successfully!")

    @require_login
    def react_to_post(self) -> None:
        posts = DataManager.get_posts()
        sample_posts = random.sample(list(posts.keys()), min(5, len(posts)))

        print("\n--- Random Posts ---")
        for pid in sample_posts:
            print(f"Post ID {pid} by @{posts[pid]['username']}: {posts[pid]['content']}")

        pid = self._get_input("\nSelect Post ID (or 'back' to cancel): ", lambda x: x in posts or print("✗ Invalid Post ID!") or False)
        if pid == "back":
            return

        reaction_actions = {
            "1": lambda: ReactionManager.add_like(pid, self.current_user.username),
            "2": lambda: ReactionManager.add_comment(pid, self.current_user.username, input("Your comment: "))
        }

        choice = input("\n1. Like\n2. Comment\nChoose: ")
        if choice in reaction_actions:
            reaction_actions[choice]()
        else:
            print("✗ Invalid choice!")

    def show_post_details(self) -> None:
        posts = DataManager.get_posts()
        reactions = DataManager.get_reactions()
        pid = self._get_input("\nEnter Post ID (or 'back' to cancel): ", lambda x: x in posts or print("✗ Post not found!") or False)
        if pid == "back":
            return

        post = posts[pid]
        likes = reactions.get(pid, {}).get("likes", [])
        comments = reactions.get(pid, {}).get("comments", [])

        print(f"\n{'='*40}\nPost by @{post['username']}\nContent: {post['content']}\nPosted: {post['time']}\n{'='*40}")
        print(f"\n👍 Likes: {len(likes)}")
        if likes:
            print(f"Liked by: {', '.join(['@' + u for u in likes])}")

        print(f"\n💬 Comments: {len(comments)}")
        for c in comments:
            print(f"  @{c['username']}: {c['text']}")
        print("="*40)

    @require_login
    def analytics(self) -> None:
        AnalyticsEngine.user_analytics(self.current_user.username)

    @require_login
    def view_profile(self) -> None:
        print(f"\n{'='*40}\n       YOUR PROFILE\n{'='*40}")
        print(f"Username: {self.current_user.username}\nName: {self.current_user.name}")
        print(f"Email: {self.current_user.email}\nSkills: {', '.join(self.current_user.skills)}\n{'='*40}")

    def logout(self) -> None:
        print(f"Goodbye, @{self.current_user.username}!")
        self.current_user = None

    def menu(self) -> None:
        print(f"\n{'='*40}\n  WELCOME TO SOCIAL MEDIA APP\n{'='*40}")

        while True:
            menu = self.user_menu if self.current_user else self.guest_menu
            
            print("\n--- Main Menu ---")
            if self.current_user:
                print(f"Logged in as: @{self.current_user.username}")
            
            for key, (label, _) in menu.items():
                print(f"{key}. {label}")

            choice = input("\nChoose: ")
            if choice in menu:
                menu[choice][1]()
            else:
                print("✗ Invalid choice!")