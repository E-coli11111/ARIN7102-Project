import spacy
import torch
from spellchecker import SpellChecker
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import json
import re

blacklist = {
    "the", "and", "is", "in", "to", "a", "of", "for", "on", "with",
    "this", "that", "it", "as", "an", "by", "at", "from", "be",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "decade", "century", "year", "month", "week", "day",
    "time", "hour", "minute", "second", "morning", "afternoon", "evening", "night",
    "monthly", "weekly", "daily", "yearly", "hourly", "minutely", "secondly",
    "fridays",
    "accountant", "accountants",
}


# device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = KeyBERT('distilbert-base-nli-mean-tokens')

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000  

def extract_keywords_bert(text, top_n=10, diversity=0.5):
    '''
    Input:
        text: str, the input text from which to extract keywords
        top_n: int, the number of keywords to extract
        diversity: float, the diversity of the keywords
    Output:
        list: A list of extracted keywords
    '''
    doc = nlp(text)
    candidates = [
        token.text.lower() for token in doc 
        if not token.is_stop 
        and not token.is_punct 
        and token.pos_ in {'NOUN', 'PROPN', 'ADJ'}
        and len(token.text) < 13
        and re.match(r'^[a-zA-Z0-9]+$', token.text)
        and token.text.lower() not in blacklist
    ]
    
    spell = SpellChecker()

    # Remove misspelled words
    candidates = list(set(candidates)) 
    candidates = [word for word in candidates if word in spell]
    # print(candidates)
    
    keywords = model.extract_keywords(text, candidates, keyphrase_ngram_range=(1, 1), use_maxsum=True, top_n=top_n, diversity=diversity)
    
    return [kw[0] for kw in keywords]

path = "data"

if __name__ == "__main__":
    f = open("keyword/keywords.jsonl", "w", encoding='utf-8')
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".md"):
                print(f"Processing {filename}...")
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    # text = preprocess_text(text)
                    # tokens = tokenize_text(text)
                    keywords = extract_keywords_bert(text)
                print(f"Extracted keywords: {keywords}")
                f.write(json.dumps({
                    "filename": filename,
                    "keywords": keywords
                }, ensure_ascii=False) + "\n")
            
    f.close()
    print("Keywords extracted and saved to keywords.jsonl")