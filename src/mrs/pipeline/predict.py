from mrs.components.data_transformation import 
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# In src/mrs/pipeline/predict.py
from pathlib import Path

class PredictionConfig:
    def __init__(self):
        # Use relative paths from the root of the project
        base_path = Path(__file__).parent.parent.parent.parent
        self.prediction_data_path = base_path / 'artifacts/processed/data/transformed_data.npy'
        self.prediction_model_path = base_path / 'artifacts/processed/models/transformer.pkl'


class Prediction:
    def __init__(self):
                # In src/mrs/pipeline/predict.py
        class Prediction:
            def __init__(self):
                try:
                    self.config = PredictionConfig()
                    if not self.config.prediction_model_path.exists():
                        raise FileNotFoundError(f"Model file not found at {self.config.prediction_model_path}")
                    if not self.config.prediction_data_path.exists():
                        raise FileNotFoundError(f"Data file not found at {self.config.prediction_data_path}")
                        
                    with open(self.config.prediction_model_path, 'rb') as f:
                        self.transformer = pickle.load(f)
                    self.model_prediction_data = np.load(self.config.prediction_data_path)
                except Exception as e:
                    raise Exception(f"Failed to initialize prediction: {str(e)}")

    def start_prediction(self, text):
        try:
            # transform the raw data
            transformed_data = self.transformer.transform([text]).toarray()
            a = self.transformer.transform(pd.Series([text]))

            # Use sklearn's cosine_similarity function for efficiency
            distances = cosine_similarity(self.model_prediction_data, a).ravel()

            # Get top 5 movie indices efficiently using np.argpartition
            top_movie_index = np.argpartition(distances, -5)[-5:]

            # Sort the top indices by their actual cosine similarity value (descending order)
            top_movie_index = top_movie_index[np.argsort(distances[top_movie_index])[::-1]]
            return top_movie_index
        except Exception as e:
            raise Exception(f'Error predicting: {e}')