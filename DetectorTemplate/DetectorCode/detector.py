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

        for user in session_data.users:
            bot_status = True 
            confidence = 50

            marked_accounts.append(DetectionMark(user_id=user['id'], confidence=confidence, bot=bot_status))

        return marked_accounts






