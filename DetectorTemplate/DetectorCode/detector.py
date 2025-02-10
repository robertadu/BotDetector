from abc_classes import ADetector
from teams_classes import DetectionMark

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        # Example:
        marked_account = []

        for user in session_data.users:

            bot_features = 0 


            # Bot is in username, you're cut 
            if "bot" in user['username'].lower() | "bot" in user['name'].lower():
                bot_features += 1 

            # Numeric heavy username 
            if sum(c.isdigit() for c in user["username"]) > 5:
                bot_features += 1

            # Empty profile description 
            if user["description"].strip() == "":
                bot_features += 1

            # High tweet count 
            if user['tweet_count'] > 90:
                bot_symptoms += 1 
            
            # Extreme z-score 
            if user['z_score'] > 3:
                bot_features += 1
            
            # If a user has more than half, then is a bot 

            bot_status = bot_features >= 3

    
            marked_account.append(DetectionMark(user_id=user['id'], confidence=50, bot=bot_status))

            return marked_account
    