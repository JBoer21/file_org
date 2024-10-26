from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import normalize
import numpy as np

# to start, we will only consider pdfs and docx


class DocumentClassifier:
    def __init__(self, threshold=0.3):
        # tf-idf is term frequency * inverse document frequency. helps us understand how important a given token / word is in classifying a document
        self.name_vectorizer = TfidfVectorizer(analyzer='word')
        self.content_vectorizer = TfidfVectorizer(analyzer='word')
        self.classifier = MultinomialNB()
        self.threshold = threshold
        self.existing_categories = []
    
    def process_folder(self, folder_path):
        ''' General idea here is that we want to create the largest 'dataset' possible for each folder. We will recursively go through all 'loose' documents in the folder and use this
        data to help classify the folder category'''
        names = [] # folder names
        contents = [] # folder documents
        categories = [] # folder names
        # Process existing folders here
        return names, contents, categories
    
    def fit(self, folder_path):
        # Get training data from existing folders
        names, contents, categories = self.process_folder(folder_path)
        
        # Create feature matrices
        name_features = self.name_vectorizer.fit_transform(names)
        content_features = self.content_vectorizer.fit_transform(contents)
        
        # Combine features (with weights)
        combined_features = np.hstack([
            name_features.toarray() * 0.4,  # Weight for name importance
            content_features.toarray() * 0.6 # Weight for content importance
        ])
        
        # Train classifier
        self.classifier.fit(combined_features, categories)
