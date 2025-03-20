from abc_classes import ADetector
from teams_classes import DetectionMark
import json 
import requests 
import pandas as pd 
import numpy as np


class Detector(ADetector):
    def detect_bot(self, session_data):

        # Displaying data for testing purposes 
        post_data = json.dumps(session_data.posts, indent=4)
        user_data = json.dumps(session_data.users, indent=4)

        # print("Post Data:", post_data)
        # print("User Data:", user_data)

        # Writing post data 14 to a file to use later 
        # with open('post_data.json', 'w') as f: 
        #    json.dump(session_data.posts, f)

        # Writing user data 14 to a file to use later 
        # with open('user_data.json', 'w') as f: 
        #    json.dump(session_data.users, f)

        marked_account = []

        for user in session_data.users:
            marked_account.append(DetectionMark(user_id=user['id'], confidence=50, bot=False))

        return marked_account


# class Detector(ADetector):
    
#     def __init__(self):
#         self.model = pickle.load(open('logisticRegressor.pkl', 'rb'))

#     def detect_bot(self, session_data):
#         marked_accounts = []

#         for user in session_data.users:
#             # create input features vector
#             features = np.array([
#                 user['username'],
#                 user['tweet_count'],
#                 user['z_score'],
#             ]).reshape(-1, 1)

#             # make prediction
#             bot_status_probabilty = self.model.predict_proba(features) # maybe wrong shape here 

#             bot_status = True if bot_status_probabilty > 0.5 else False

#             marked_accounts.append(DetectionMark(user_id=user['id'], confidence=bot_status_probabilty, bot=bot_status))

#         return marked_accounts

# class Detector(ADetector):
    
#     def __init__(self):
#         self.model = pickle.load(open("logisticRegressor.pkl", "rb"))
#         print("Model expects features:", self.model.feature_names_in_)  # Debugging

#     def detect_bot(self, session_data):
#         marked_accounts = []

#         for user in session_data.users:
                
#                 # print(session_data.users)

#                 df = pd.DataFrame(session_data.users)
#                 label_encoder = LabelEncoder()
#                 df["username_encoded"] = label_encoder.fit_transform(df["username"])
#                 # print(df)
                
         
#                 # Extract feature names from the trained model
#                 # expected_features = self.model.feature_names_in_

#                 # # Dynamically build feature vector
#                 # features = np.array([
#                 #     (user[feature].astype(int)) for feature in expected_features
#                 # ]).reshape(1, -1)

#                 # print("Features:", features)  # Debugging
#                 # print("Feature dtypes:", [type(f) for f in features.flatten()])

#                 # create input features vector
#                 features = np.array([
#                     df['username_encoded'],
#                     df['tweet_count'],
#                     df['z_score'],
#                 ]).reshape(-1, 1)



#                 # Make prediction
#                 bot_status_probability = self.model.predict_proba(features)[0][1]  # Get probability of bot class

#                 bot_status = bot_status_probability > 0.5  # Convert probability to boolean
        
#                 marked_accounts.append(
#                     DetectionMark(
#                         user_id=user['id'], 
#                         confidence=bot_status_probability, 
#                         bot=bot_status
#                     )
#                 )

#         return marked_accounts

# class Detector(ADetector):
    
#     def __init__(self):
#         self.model = pickle.load(open("logisticRegressor.pkl", "rb"))
#         print("Model expects features:", self.model.feature_names_in_)  # Debugging

#     def detect_bot(self, session_data):
#         marked_accounts = []

#         # Convert session_data.users into a DataFrame
#         df = pd.DataFrame(session_data.users)

#         # Ensure required features exist
#         required_features = ['username', 'tweet_count', 'z_score']
#         if not all(col in df.columns for col in required_features):
#             raise ValueError(f"Missing required features: {set(required_features) - set(df.columns)}")

#         # Encode username **once** (before looping)
#         label_encoder = LabelEncoder()
#         df["username_encoded"] = label_encoder.fit_transform(df["username"])

#         # Keep only required columns
#         df = df[['username_encoded', 'tweet_count', 'z_score']]
#         print("Processed DataFrame:\n", df.head())  # Debugging

#         # Loop through each user and predict bot status
#         for _, user in df.iterrows():
#             # Convert row to NumPy array with correct shape (1, 3)
#             features = user.values.reshape(1, -1)  # ✅ Now it has shape (1, 3)

#             # Make prediction
#             bot_status_probability = self.model.predict_proba(features)[0][1]  # Get probability of bot class
#             bot_status = bot_status_probability > 0.5  # Convert probability to boolean

#             # Append detection result
#             marked_accounts.append(
#                 DetectionMark(
#                     user_id=user['username_encoded'],  # Assuming user_id is username_encoded
#                     confidence=bot_status_probability, 
#                     bot=bot_status
#                 )
#             )

#         return marked_accounts


# import pickle
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder

# class Detector(ADetector):
    
#     def __init__(self):
#         self.model = pickle.load(open("logisticRegressor.pkl", "rb"))
#         print("Model expects features:", self.model.feature_names_in_)  # Debugging

#     def detect_bot(self, session_data):
#         marked_accounts = []

#         # Convert session_data.users into a DataFrame
#         df = pd.DataFrame(session_data.users)

#         # Ensure required features exist
#         required_features = ['username', 'tweet_count', 'z_score']
#         if not all(col in df.columns for col in required_features):
#             raise ValueError(f"Missing required features: {set(required_features) - set(df.columns)}")

#         # Encode username **once** (before looping)
#         label_encoder = LabelEncoder()
#         df["username"] = label_encoder.fit_transform(df["username"]).astype(str)  # Ensure it's a string

#         # Keep only required columns and ensure they match model features
#         df = df[['username', 'tweet_count', 'z_score']]
#         df.columns = self.model.feature_names_in_  # Ensure column names match

#         print("Processed DataFrame:\n", df.head())  # Debugging

#         # Loop through each user and predict bot status
#         for i, user in df.iterrows():
#             # Convert row to NumPy array with correct shape (1, 3)
#             features = user.values.reshape(1, -1)

#             # Make prediction
#             bot_status_probability = self.model.predict_proba(features)[0][1]  # Get probability of bot class
#             bot_status = bot_status_probability > 0.5  # Convert probability to boolean

#             # Ensure `user_id` is a string, and `confidence` is an integer
#             user_id = str(session_data.users[i]['id'])  # Ensure user_id is a string
#             confidence = int(bot_status_probability * 100)  # Convert probability to int percentage

#             # Append detection result
#             marked_accounts.append(
#                 DetectionMark(
#                     user_id=user_id,  # Now it's a string
#                     confidence=confidence,  # Now it's an integer
#                     bot=bot_status
#                 )
#             )

#         return marked_accounts








