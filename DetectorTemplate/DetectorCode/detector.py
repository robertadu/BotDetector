from abc_classes import ADetector
from teams_classes import DetectionMark
import pickle 
import pandas as pd 
import numpy as np 
from datetime import datetime
from collections import Counter
from textblob import TextBlob

class Detector(ADetector):

    def detect_bot(self, session_data):
        marked_accounts = []

        # Load the model
        with open("logistic_regression_model-2.pkl", "rb") as model_file:
            model = pickle.load(model_file)

        # Load the scaler
        with open("scaler-2.pkl", "rb") as scaler_file:
            scaler = pickle.load(scaler_file)

        # Transforming the data into a pandas dataframe 
        session_df = pd.DataFrame(session_data.users)

        df_posts = pd.DataFrame(session_data.posts)
        df_users = pd.DataFrame(session_data.users)
        df_users.rename(columns={"id": "user_id"}, inplace=True)

        df = pd.merge(df_posts, df_users, left_on='author_id', right_on='user_id')

        # Extract features and scale 
        X_session = extract_features(df)
        X_session_scaled = scaler.transform(X_session)

        # Predict bot probabilities and labels
        bot_probs = model.predict_proba(X_session_scaled)[:, 1]
        bot_labels = model.predict(X_session_scaled)

        df['bot_prob'] = bot_probs
        df['bot_label'] = bot_labels    

        # Create DetectionMark objects
        for user_id, group in df.groupby('user_id'):
            avg_prob = group['bot_prob'].mean()
            majority_label = round(group['bot_label'].mean())  # round() gives majority vote

            marked_accounts.append(DetectionMark(user_id=user_id, confidence=int(avg_prob * 100), bot=bool(majority_label)))

        # Tesing Code 
        # for account in marked_accounts:
        #     print(f"User ID: {account.user_id}, Bot: {account.bot}, Confidence: {account.confidence}%")

        return marked_accounts
    
    # Time Entropy (Measures randomness in posting times)
def time_entropy(times):
    counts = Counter(times.dt.hour)
    probabilities = np.array(list(counts.values())) / sum(counts.values())
    return -np.sum(probabilities * np.log2(probabilities + 1e-10))

# Feature Extraction Function
def extract_features(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'].dt.tz_localize(None)
    df['account_age'] = (datetime.today() - df['created_at']).dt.days
    df['tweets_per_day'] = df['tweet_count'] / (df['account_age'] + 1)

    df['burstiness_score'] = df.groupby('user_id')['created_at'].transform(
        lambda x: (x.diff().dt.total_seconds().std() / (x.diff().dt.total_seconds().mean() + 1)))
    df['time_entropy'] = df.groupby('user_id')['created_at'].transform(time_entropy)

    df['unique_words'] = df['text'].apply(lambda x: len(set(x.split())))
    df['total_words'] = df['text'].apply(lambda x: len(x.split()))
    df['lexical_diversity'] = df['unique_words'] / (df['total_words'] + 1)

    df['tweet_length'] = df['text'].apply(len)
    df['avg_tweet_length'] = df.groupby('user_id')['tweet_length'].transform('mean')

    df['hashtag_count'] = df['text'].str.count(r"#\\w+")
    df['hashtag_count_per_tweet'] = df.groupby('user_id')['hashtag_count'].transform('mean')

    df['punctuation_ratio'] = df['text'].apply(lambda x: sum(1 for c in x if c in '!?.,;') / (len(x) + 1))
    stopwords = set("the and is in to of a that it on for with as was at by an this be or are from which one were all have has would not if there their can more when who what about its".split())
    df['stopword_ratio'] = df['text'].apply(lambda x: sum(1 for word in x.split() if word.lower() in stopwords) / (len(x.split()) + 1))

    df['sentiment_score'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    df['text_repetition_score'] = df.groupby('user_id')['text'].transform(lambda x: sum(x.duplicated()) / len(x))
    df['hashtag_reuse_score'] = df.groupby('user_id')['hashtag_count'].transform(lambda x: sum(x.duplicated()) / len(x))

    features = [
        'z_score', 'tweets_per_day', 'avg_tweet_length',
        'lexical_diversity', 'hashtag_count_per_tweet',
        'burstiness_score', 'time_entropy', 'punctuation_ratio',
        'stopword_ratio', 'sentiment_score', 'text_repetition_score', 'hashtag_reuse_score',
        'account_age'
    ]

    return df[features].fillna(0)








