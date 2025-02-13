from abc_classes import ADetector
from teams_classes import DetectionMark

class Detector(ADetector):
    def detect_bot(self, session_data):
        marked_accounts = []

        # print(session_data)

        for user in session_data.users:
            bot_features = 0 

            # "bot" is in username or display name
            if "bot" in user['username'].lower() or "bot" in user['name'].lower():
                bot_features += 1 

            # Numeric-heavy username
            if sum(c.isdigit() for c in user["username"]) > 5:
                bot_features += 1

            # Empty profile description
            if user["description"].strip() == "":
                bot_features += 1

            # High tweet count
            if user['tweet_count'] > 90:
                bot_features += 1 
            
            # Extreme z-score
            if user['z_score'] > 3:
                bot_features += 1
            
            # Repetitive conent 
            unique_texts = set(post["text"].lower().strip() for post in session_data.posts)
            if len(session_data.posts) > 10 and len(unique_texts) / len(session_data.posts) < 0.5:  # More than 50% repetition
                bot_features += 1

            # High post frequency
            user_posts = [post for post in session_data.posts if post["author_id"] == user["id"]]
            if len(user_posts) > 2:
                timestamps = [post["created_at"] for post in user_posts]
                time_diffs = [(int(timestamps[i + 1][14:16]) - int(timestamps[i][14:16])) for i in range(len(timestamps) - 1)]
                avg_time_between_posts = sum(time_diffs) / len(time_diffs) if time_diffs else 100
                
                if avg_time_between_posts < 2:  # Less than 2 mins between posts
                    bot_features += 1
            
            # If a user has more than half of the checks, mark as a bot
            bot_status = bot_features >= 3

            marked_accounts.append(DetectionMark(user_id=user['id'], confidence=50, bot=bot_status))

        return marked_accounts  # Move return outside loop
