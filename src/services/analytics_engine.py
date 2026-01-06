from .data_manager import DataManager


class AnalyticsEngine:
    @staticmethod
    def user_analytics(username: str) -> None:
        posts = DataManager.get_posts()
        reactions = DataManager.get_reactions()

        user_posts = {pid: pdata for pid, pdata in posts.items() if pdata["username"] == username}
        
        engagement = {
            pid: len(reactions.get(pid, {}).get("likes", [])) + 
                 len(reactions.get(pid, {}).get("comments", []))
            for pid in user_posts
        }

        total_likes = sum(len(reactions.get(pid, {}).get("likes", [])) for pid in user_posts)
        total_comments = sum(len(reactions.get(pid, {}).get("comments", [])) for pid in user_posts)
        most_engaged = max(engagement, key=engagement.get) if engagement else None

        print(f"\n{'='*40}\n       USER ANALYTICS\n{'='*40}")
        print(f"Username: {username}\nTotal Posts: {len(user_posts)}")
        print(f"Total Likes Received: {total_likes}\nTotal Comments Received: {total_comments}")
        
        if most_engaged:
            print(f"\nMost Engaged Post ID: {most_engaged}\nEngagement Count: {engagement[most_engaged]}")
        print("="*40)