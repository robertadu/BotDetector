from abc_classes import ADetector
from teams_classes import DetectionMark

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        # Example:
        marked_account = []
        

        for user in session_data.users:

            bot_status = False

            username = user["username"]

            if username == "I_am_a_bot":
                bot_status = True
    
            marked_account.append(DetectionMark(user_id=user['id'], confidence=50, bot=bot_status))

        return marked_account
    