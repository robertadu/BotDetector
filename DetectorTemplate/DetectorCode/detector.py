from abc_classes import ADetector
from teams_classes import DetectionMark
import json 
import datetime 
import math 
import statistics
import re

class Detector(ADetector):

    def detect_bot(self, session_data):
        marked_accounts = []

        # Comment out print statements before pushing to repo
        # print("Users:", json.dumps(session_data.users, indent = 4))
        # print("Posts:", json.dumps(session_data.posts, indent = 4))


        for user in session_data.users:
            bot_features = 0 

            username = user['username'].lower()
            display_name = user['name'].lower()
            description = user["description"].strip()
            tweet_count = user['tweet_count']
            z_score = user['z_score']

            user_posts = [post for post in session_data.posts if post["author_id"] == user["id"]]

            # Username contains "bot" variations
            if "bot" in username or "b0t" in username or "bot_" in username or "bot123" in username:
                bot_features += 1 
            if "bot" in display_name or "b0t" in display_name:
                bot_features += 1 

            # Numeric-heavy username (More than 50% digits)
            digit_count = sum(1 for c in username if c.isdigit())
            if digit_count / len(username) > 0.5:
                bot_features += 1

            # Empty or very short profile description
            if len(description) < 10:
                bot_features += 1

            # Random character username detection
            if len(username) > 6:
                unique_chars = len(set(username))
                if unique_chars / len(username) > 0.8:  
                    bot_features += 1

            # Estimate account age using first post timestamp
            first_post_date = None

            for post in user_posts:
                post_date = post["created_at"].split("T")[0]  # Extract "YYYY-MM-DD"
                if first_post_date is None or post_date < first_post_date:
                    first_post_date = post_date

            if first_post_date:
                created_date = first_post_date.split("T")[0]  # Extract "YYYY-MM-DD"
                created_year, created_month, created_day = map(int, created_date.split("-"))
                
                # Manually set today's date
                current_year, current_month, current_day = 2025, 2, 20  

                age_in_days = (current_year - created_year) * 365 + (current_month - created_month) * 30 + (current_day - created_day)
                if age_in_days < 1:
                    age_in_days = 1  

                tweets_per_day = tweet_count / age_in_days
                if tweets_per_day > 20:  
                    bot_features += 1

            # Extreme z-score
            if z_score > 2:
                bot_features += 1

            # Repetitive content check (User-specific)
            unique_texts = set(post["text"].strip().lower() for post in user_posts)
            if len(user_posts) > 10 and len(unique_texts) / len(user_posts) < 0.5:
                bot_features += 1

            # High posting frequency (Less than 2 mins average gap between posts)
            if len(user_posts) > 3:
                timestamps = [post["created_at"].split("T")[1][:8] for post in user_posts]  # Extract "HH:MM:SS"
                timestamps = [list(map(int, t.split(":"))) for t in timestamps]  # Convert to [HH, MM, SS]

                time_diffs = []
                for i in range(len(timestamps) - 1):
                    h1, m1, s1 = timestamps[i]
                    h2, m2, s2 = timestamps[i + 1]

                    diff = (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)  # Convert to seconds
                    if diff > 0:
                        time_diffs.append(diff / 60)  # Convert to minutes

                avg_time_between_posts = sum(time_diffs) / len(time_diffs) if time_diffs else 100
                if avg_time_between_posts < 2:  # Less than 2 minutes between posts
                    bot_features += 1

            # Check for identical post beginnings
                if len(user_posts) >= 5:
                    beginnings = [post["text"][:15].lower() for post in user_posts]
                    unique_beginnings = set(beginnings)
                    
                    if len(unique_beginnings) / len(beginnings) < 0.4:
                        bot_features += 1

            # Determine bot status based on bot features
            bot_status = bot_features >= 2

            # Dynamic confidence score (scales with bot indicators)
            confidence = min(100, bot_features * 20)

            marked_accounts.append(DetectionMark(user_id=user['id'], confidence=confidence, bot=bot_status))

        return marked_accounts




