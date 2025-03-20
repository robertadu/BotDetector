from abc_classes import ADetector
from teams_classes import DetectionMark
import json 
import pickle 
import pandas as pd 
import numpy as np 


class Detector(ADetector):

    def detect_bot(self, session_data):
        marked_accounts = []

        # Load the model
        with open("logistic_regression_model.pkl", "rb") as model_file:
            model = pickle.load(model_file)

        # Load the scaler
        with open("scaler.pkl", "rb") as scaler_file:
            scaler = pickle.load(scaler_file)

        # Transforming the data into a pandas dataframe 
        session_df = pd.DataFrame(session_data.users)
        # print(session_df)

        # Scale the new data using the loaded scaler
        session_df.rename(columns={"id": "user_id"}, inplace=True)
        X_session = session_df[['tweet_count', 'z_score']]  
        X_session_scaled = scaler.transform(X_session)

        # Get probability of bot 
        bot_probs = model.predict_proba(X_session_scaled)[:, 1]

        # Get binary predictions 
        bot_labels = model.predict(X_session_scaled)

        # Creating the annotated dataset 
        for user_id, bot, prob in zip(session_df['user_id'], bot_labels, bot_probs):
            marked_accounts.append(DetectionMark(user_id=user_id, confidence=int(prob * 100), bot=bool(bot)))

        return marked_accounts






