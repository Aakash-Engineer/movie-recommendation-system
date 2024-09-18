import os
import sys
from dataclasses import dataclass
import re
import ast
import nltk
import string
import numpy as np
import pandas as pd
from textblob import TextBlob
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pickle


@dataclass
class DataTransformationConfig:
    raw_data_path = 'artifacts/raw/movies.csv'
    processed_data_dir = 'artifacts/processed/data/'
    processed_model_dir = 'artifacts/processed/models/'

class BasicTextPreprocessing:  
    def __init__(self):  
        pass 

    def fit(self, X, y=None):
        self.config = DataTransformationConfig()
        return self
        
    def transform(self, X, y=None):  
        
        def keep_text_only(input_string):   
            result = re.findall(r'[a-zA-Z\s]+', input_string)   
            return ''.join(result).strip()    
        
        def remove_urls(text):    
            if isinstance(text, str):  # Check if the text is a string  
                url_pattern = r'\b(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?\b'    
                cleaned_text = re.sub(url_pattern, '', text)   
                return ' '.join(cleaned_text.split())  
            return text  # Return as is for non-string inputs  
            
        def remove_punctuation(row):   
            return row.translate(str.maketrans('', '', string.punctuation)) 

        def spell_correction(row):
            l = []
            for i in row.split():
                l.append(str(TextBlob(i).correct()))
            return ' '.join(l)
            
        def remove_stopwords(text):
            stop_words = set(stopwords.words('english'))
            return ' '.join([i for i in text.split() if i.lower() not in stop_words])

        def lemmatization(row):  
            lemmatizer = WordNetLemmatizer()
            l = [lemmatizer.lemmatize(i) for i in row.split()]  
            return ' '.join(l)
            
        X = X.str.lower()  
        X = X.apply(keep_text_only)  
        X = X.apply(remove_urls)  
        X = X.apply(remove_punctuation)    
        X = X.apply(remove_stopwords)  
        X = X.apply(lemmatization)
        return X.values
        
class DataTransformation:
    def __init__(self) -> None:
        self.config = DataTransformationConfig()

    def start_transformation(self):
        try:
            df = pd.read_csv(self.config.processed_data_path)
            transformer = Pipeline(steps=[
                ('basic preprocessing', BasicTextPreprocessing()),
                ('count vectorization', CountVectorizer(max_features=10000)),
                ('tf-idf', TfidfTransformer())
            ])
            transformed_data = transformer.transform(df['tags']).toarray()
            with open(self.config.processed_model_dir + 'transformer.pkl', 'wb') as f:
                pickle.dump(transformer, f)
            # store numpy array to disk
            np.save(self.config.processed_data_dir + 'transformed_data.npy', transformed_data)
        except Exception as e:
            raise Exception(f'Error transforming data: {e}')
        
        
# tokenizer = Pipeline(steps=[
#     ('basic preprocessing', BasicTextPreprocessing()),
#     ('count vectorization', CountVectorizer(max_features=10000)),
#     ('tf-idf', TfidfTransformer())
#     # ('cosign similarity', CosineSimilarity())
# ])

# # Assuming df is defined AttributeErrorand 'tags' is a column
# similarity = tokenizer.fit_transform(new_df['tags']).toarray() # Fixed for Series input

# def recommend(text):
#     a = tokenizer.transform(pd.Series([text]))
#     distances = np.dot(similarity, a.T).ravel()/(np.linalg.norm(similarity, axis=1)*(np.linalg.norm(a)))
#     top_movie_index = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     return top_movie_index
# recommend('a horror movie with love story and romance')

