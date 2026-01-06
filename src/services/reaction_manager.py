from .data_manager import DataManager, REACTION_FILE


class ReactionManager:
    @staticmethod
    def add_like(post_id: str, username: str) -> bool:
        reactions = DataManager.get_reactions()
        reactions.setdefault(post_id, {"likes": [], "comments": []})
        
        if username in reactions[post_id]["likes"]:
            print("You already liked this post!")
            return False
        
        reactions[post_id]["likes"].append(username)
        DataManager.save(REACTION_FILE, reactions)
        print(f"✓ {username} liked the post!")
        return True

    @staticmethod
    def add_comment(post_id: str, username: str, text: str) -> None:
        reactions = DataManager.get_reactions()
        reactions.setdefault(post_id, {"likes": [], "comments": []})
        
        reactions[post_id]["comments"].append({"username": username, "text": text})
        DataManager.save(REACTION_FILE, reactions)
        print("✓ Comment added!")