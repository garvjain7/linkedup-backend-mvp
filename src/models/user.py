from typing import Dict, List, Optional


class User:
    def __init__(self, username: str, name: str, email: str, skills: List[str], user_id: Optional[int] = None):
        self.username = username
        self.user_id = user_id or self._generate_user_id()
        self.name = name
        self.email = email
        self.skills = skills

    def _generate_user_id(self) -> int:
        from ..services.data_manager import DataManager  # Import here to avoid circular
        users = DataManager.get_users()
        return max([u["user_id"] for u in users.values()], default=0) + 1

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    def _edit_skills(self) -> List[str]:
        new_skills = []
        for i, current_skill in enumerate(self.skills, 1):
            while True:
                new_skill = input(f"Skill {i} (current: {current_skill}). To keep the same, press Enter (or 'back' to cancel all changes): ").strip()
                if new_skill == "":
                    new_skills.append(current_skill)
                    break
                elif new_skill == "back":
                    return self.skills  # Cancel, return unchanged
                elif new_skill:
                    new_skills.append(new_skill)
                    break
        return new_skills

    def edit_profile(self) -> None:
        actions = {
            "1": ("Name", lambda: input("New name: ")),
            "2": ("Email", lambda: input("New email: ")),
            "3": ("Skills", self._edit_skills)
        }

        while True:
            print("\n--- Edit Profile ---")
            for key, (label, _) in actions.items():
                print(f"{key}. {label}")
            print("4. Exit")

            choice = input("Choose: ")
            if choice == "4":
                break
            if choice in actions:
                attr_name = actions[choice][0].lower()
                setattr(self, attr_name, actions[choice][1]())
            else:
                print("Invalid choice!")

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(**data)