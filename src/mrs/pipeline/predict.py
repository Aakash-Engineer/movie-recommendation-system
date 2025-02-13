import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# In src/mrs/pipeline/predict.py
from pathlib import Path

# src/mrs/pipeline/predict.py
class PredictionConfig:
    def __init__(self):
        # Use relative paths that will work on Streamlit Cloud
        self.prediction_data_path = Path('artifacts/processed/data/transformed_data.npy')
        self.prediction_model_path = Path('artifacts/processed/models/transformer.pkl')


# src/mrs/pipeline/predict.py
import logging

class Prediction:
    def __init__(self):
        try:
            self.config = PredictionConfig()
            logging.info(f"Looking for model at: {self.config.prediction_model_path}")
            logging.info(f"Looking for data at: {self.config.prediction_data_path}")
            
            if not self.config.prediction_model_path.exists():
                raise FileNotFoundError(f"Model file not found at {self.config.prediction_model_path}")
            if not self.config.prediction_data_path.exists():
                raise FileNotFoundError(f"Data file not found at {self.config.prediction_data_path}")
            
            with open(self.config.prediction_model_path, 'rb') as f:
                self.transformer = pickle.load(f)
            self.model_prediction_data = np.load(self.config.prediction_data_path)
            
        except Exception as e:
            logging.error(f"Failed to initialize prediction: {str(e)}")
            raise Exception(f"Failed to initialize prediction: {str(e)}")

        # src/mrs/pipeline/predict.py
    def start_prediction(self, text):
        try:
            # Transform the raw data
            transformed_data = self.transformer.transform([text]).toarray()
            a = self.transformer.transform(pd.Series([text]))
            
            # Calculate cosine similarity
            distances = cosine_similarity(self.model_prediction_data, a).ravel()
            
            # Get top 5 indices
            top_movie_index = np.argpartition(distances, -5)[-5:]
            top_movie_index = top_movie_index[np.argsort(distances[top_movie_index])[::-1]]
            
            return top_movie_index
            
        except Exception as e:
            logging.error(f"Error in prediction: {str(e)}")
            raise Exception(f"Error in prediction: {str(e)}")