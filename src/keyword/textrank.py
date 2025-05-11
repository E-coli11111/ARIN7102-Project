from rake_nltk import Rake
import nltk
import os
import json
import re
import string
from nltk.tokenize import sent_tokenize
import time

nltk.download('stopwords')
nltk.download('punkt_tab')

def preprocess_text(text):
    """
    Preprocess the text by removing non-ASCII characters and converting to lowercase.
    
    Parameters:
    text (str): The input text to preprocess.
    
    Returns:
    str: The preprocessed text.
    """
    # Remove markdown syntax
    text = text.replace("#", "").replace("##", "").replace("###", "").replace("####", "").replace("#####", "").replace("######", "")
    
    # Remove table of contents
    text = re.sub(r'<.*?>', '', text)
    # text = re.sub(r'< td >', '', text)
    
    # Remove non-ASCII characters
    text = ''.join(filter(lambda x: x in string.printable, text))
    
    # Convert to lowercase
    text = text.lower()
    
    return text

def extract_keywords(text, max_words=3):
    """
    Extract keywords from the given text using RAKE algorithm.
    
    Parameters:
    text (str): The input text from which to extract keywords.
    max_words (int): The maximum number of words allowed in a keyword.
    
    Returns:
    list: A list of tuples containing the keyword and its score.
    """
    # Initialize RAKE
    rake = Rake(stopwords={".", "#", "##", "###"}, sentence_tokenizer=sent_tokenize, word_tokenizer=nltk.word_tokenize)
    
    # Extract keywords
    rake.extract_keywords_from_text(text)
    
    # Get ranked phrases with scores
    ranked_phrases_with_scores = rake.get_ranked_phrases_with_scores()
    
    # Filter out phrases longer than max_words
    filtered_keywords = [
        (score, phrase) for score, phrase in ranked_phrases_with_scores
        if len(phrase.split()) <= max_words
    ]
    
    # Sort keywords by score in descending order and return top 5
    sorted_keywords = sorted(filtered_keywords, key=lambda x: x[0], reverse=True)[:20]
    
    return sorted_keywords

path = "data"

if __name__ == "__main__":
    start_time = time.time()  # Start timing
    cnt = 0
    f = open("keyword/keywords_textrank.jsonl", "w", encoding='utf-8')
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".md"):
                print(f"Processing {filename}...")
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    text = preprocess_text(text)
                    keywords = extract_keywords(text)
                    
                f.write(json.dumps({
                    "filename": filename,
                    "keywords": keywords
                }, ensure_ascii=False) + "\n")
                cnt += 1
            
    f.close()
    end_time = time.time()  # End timing
    print(f"Keywords extracted and saved to keywords.jsonl in {end_time - start_time:.2f} seconds, {cnt} files processed.")