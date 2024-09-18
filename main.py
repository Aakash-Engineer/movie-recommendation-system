from mrs.components.data_ingestion import DataIngestion
from mrs.components.data_transformation import DataTransformation
from mrs.pipeline.predict import Prediction


try:
    # data_ingestion = DataIngestion()
    # data_ingestion.start_ingestion()
    # data_transformation = DataTransformation()
    # data_transformation.start_transformation()
    prediction = Prediction()
    text = 'I love this movie'
    print(prediction.start_prediction(text))
    
except Exception as e:
    raise e