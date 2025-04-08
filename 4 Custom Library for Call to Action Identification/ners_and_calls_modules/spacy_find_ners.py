import spacy
import re

# Find 4 big letters in a row
regex = r"\b[A-Z]{4}\b"

def find_ner_firms(text: str, nlp_rus: spacy.lang) -> list:
    """
    The function extracts named entities with the tag 'ORG' (company names) using spaCy
    text – the text from which to extract company names
    nlp_rus – the spaCy language model
    """
    four_capital_letters = re.findall(regex, text)
    res = [org.text for org in nlp_rus(text).ents if org.label_ == 'ORG']
    return list(set([ner for ner in res] + four_capital_letters)) # using a set to ensure uniqueness