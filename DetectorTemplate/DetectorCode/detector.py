from abc_classes import ADetector
from teams_classes import DetectionMark
import json 
import datetime 
import math 
import statistics
import re

class Detector(ADetector):

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))

    def detect_bot(self, session_data):
        marked_accounts = []

        # Pre-trained weights for logistic regression
        weights = {
            "username_bot": 1.5,
            "display_name_bot": 1.2,
            "numeric_username": 1.8,
            "short_description": 1.3,
            "random_chars_username": 1.5,
            "tweets_per_day": 2.0,
            "extreme_z_score": 2.2,
            "repetitive_content": 1.7,
            "high_posting_frequency": 2.5,
            "identical_beginnings": 1.4,
            "bias": -5.0  # Adjust to tune threshold
        }

        for user in session_data.users:
            features = []  # List to store feature values

            username = user['username'].lower()
            display_name = user['name'].lower()
            description = user["description"].strip()
            tweet_count = user['tweet_count']
            z_score = user['z_score']

            user_posts = [post for post in session_data.posts if post["author_id"] == user["id"]]

            # Feature calculations
            features.append(int("bot" in username or "b0t" in username or "bot_" in username or "bot123" in username))  # username_bot
            features.append(int("bot" in display_name or "b0t" in display_name))  # display_name_bot
            
            digit_count = sum(1 for c in username if c.isdigit())
            features.append(int(digit_count / len(username) > 0.5))  # numeric_username
            
            features.append(int(len(description) < 10))  # short_description
            
            if len(username) > 6:
                unique_chars = len(set(username))
                features.append(int(unique_chars / len(username) > 0.8))  # random_chars_username
            else:
                features.append(0)

            # Estimate account age using first post timestamp
            first_post_date = None

            for post in user_posts:
                post_date = post["created_at"].split("T")[0]  # Extract "YYYY-MM-DD"
                if first_post_date is None or post_date < first_post_date:
                    first_post_date = post_date

            if first_post_date:
                created_year, created_month, created_day = map(int, first_post_date.split("-"))
                
                # Manually set today's date
                current_year, current_month, current_day = 2025, 2, 20  

                age_in_days = (current_year - created_year) * 365 + (current_month - created_month) * 30 + (current_day - created_day)
                age_in_days = max(age_in_days, 1)  

                tweets_per_day = tweet_count / age_in_days
                features.append(int(tweets_per_day > 20))  # tweets_per_day
            else:
                features.append(0)

            features.append(int(z_score > 2))  # extreme_z_score
            
            unique_texts = set(post["text"].strip().lower() for post in user_posts)
            features.append(int(len(user_posts) > 10 and len(unique_texts) / len(user_posts) < 0.5))  # repetitive_content

            # High posting frequency (Less than 2 mins avg gap)
            if len(user_posts) > 3:
                timestamps = [post["created_at"].split("T")[1][:8] for post in user_posts]  # Extract "HH:MM:SS"
                timestamps = [list(map(int, t.split(":"))) for t in timestamps]  

                time_diffs = []
                for i in range(len(timestamps) - 1):
                    h1, m1, s1 = timestamps[i]
                    h2, m2, s2 = timestamps[i + 1]

                    diff = (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)
                    if diff > 0:
                        time_diffs.append(diff / 60)

                avg_time_between_posts = sum(time_diffs) / len(time_diffs) if time_diffs else 100
                features.append(int(avg_time_between_posts < 2))  # high_posting_frequency
            else:
                features.append(0)

            # Identical post beginnings
            if len(user_posts) >= 5:
                beginnings = [post["text"][:15].lower() for post in user_posts]
                unique_beginnings = set(beginnings)
                features.append(int(len(unique_beginnings) / len(beginnings) < 0.4))  # identical_beginnings
            else:
                features.append(0)

            # Logistic Regression Calculation
            weighted_sum = sum(feature * weight for feature, weight in zip(features, weights.values()))
            bot_probability = self.sigmoid(weighted_sum)

            # Classification
            bot_status = bot_probability > 0.5  # Threshold at 50%

            # Confidence calculation
            confidence = int(bot_probability * 100)

            marked_accounts.append(DetectionMark(user_id=user['id'], confidence=confidence, bot=bot_status))

        return marked_accounts






