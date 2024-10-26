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
        """ 
        Process a root folder to collect training data from its subfolders.
        Each immediate subfolder is treated as a category.
        
        Args:
        folder_path (str): Path to the root folder containing category subfolders
            
        Returns:
            tuple: (names, contents, categories) where:
                - names: list of file names
                - contents: list of file contents
                - categories: list of corresponding categories
        """
        names = []
        contents = []
        categories = []
        
        # Get immediate subfolders (categories)
        for category in os.listdir(folder_path):
            category_path = os.path.join(folder_path, category)
            
            # Skip if not a directory
            if not os.path.isdir(category_path):
                continue
                
            # Store category for later use
            if category not in self.existing_categories:
                self.existing_categories.append(category)
            
            # Process all files in the category folder and its subfolders
            for root, _, files in os.walk(category_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip non-PDF/DOCX files
                    if not file.lower().endswith(('.pdf', '.docx')):
                        continue
                        
                    try:
                        # Extract data from file
                        title, content = self.extract_data_from_file(file_path)
                        
                        # Add to training data
                        names.append(title)
                        contents.append(content)
                        categories.append(category)
                        
                    except (ValueError, FileNotFoundError) as e:
                        print(f"Error processing {file_path}: {str(e)}")
                        continue
        
        return names, contents, categories


    def extract_data_from_file(self, file):
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
    
    def predict(self, file_path):
        """
        Predict the category for a single file.
        
        Args:
            file_path (str): Path to the file to classify
            
        Returns:
            tuple: (predicted_category, confidence_score)
        """
        title, content = self.extract_data_from_file(file_path)
        
        # Transform features
        name_feature = self.name_vectorizer.transform([title])
        content_feature = self.content_vectorizer.transform([content])
        
        # Combine features
        combined_feature = np.hstack([
            name_feature.toarray() * 0.4,
            content_feature.toarray() * 0.6
        ])
        
        # Get prediction probabilities
        probabilities = self.classifier.predict_proba(combined_feature)[0]
        
        # Get the highest probability and corresponding category
        max_prob = max(probabilities)
        predicted_category = self.existing_categories[np.argmax(probabilities)]
        
        return predicted_category, max_prob

    def organize_file(self, file_path, destination_root):
        """
        Organize a single file by moving it to the predicted category folder.
        
        Args:
            file_path (str): Path to the file to organize
            destination_root (str): Root folder where category folders exist
        """
        category, confidence = self.predict(file_path)
        
        if confidence < self.threshold:
            category = "unclassified"
        
        # Create category folder if it doesn't exist
        category_path = os.path.join(destination_root, category)
        os.makedirs(category_path, exist_ok=True)
        
        # Move file to appropriate folder
        filename = os.path.basename(file_path)
        destination = os.path.join(category_path, filename)
        os.rename(file_path, destination)

