from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import normalize
import numpy as np
from PyPDF2 import PdfReader
from docx import Document
import os

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

    def extract_data_from_file(file):
        '''
        Given a file path, extract its title and contents.
        Works only for PDF and DOCX files.
        
        Args:
            file (str): Path to the file
            
        Returns:
            tuple: (title, content) where title is the filename without extension
                and content is the extracted text
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        '''
        if not os.path.exists(file):
            raise FileNotFoundError(f"File {file} not found")
        
        # Get file extension and title
        file_extension = os.path.splitext(file)[1].lower()
        title = os.path.splitext(os.path.basename(file))[0]
        content = ""
        
        if file_extension == '.pdf':
            # Handle PDF files
            reader = PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
                
        elif file_extension == '.docx':
            # Handle DOCX files
            doc = Document(file)
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
                
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX files are supported")
        
        return title, content.strip()
