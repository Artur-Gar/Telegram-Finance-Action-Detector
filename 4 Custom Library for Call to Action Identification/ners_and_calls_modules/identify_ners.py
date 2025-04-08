import pandas as pd
from difflib import SequenceMatcher
import numpy as np

from ners_and_calls_modules.general_string_helpers import replace_several_substrs
from ners_and_calls_modules.spacy_find_ners import find_ner_firms 

def get_most_possible_firm(firm_ner: str, df_ner_firms: pd.DataFrame, cols_to_match: list = ['firm_name', 'securityid']) -> dict:
    """
    The function performs matching between a named entity and a ticker (financial instrument) that may correspond to this entity.
    
    It returns a dictionary in the form:
    {'securityid': the ticker most likely associated with the named entity, 'matching_score': a conditional matching probability (used for filtering)}
    
    Args:
    firm_ner – the named entity to match with a ticker
    df_ner_firms – a reference table of company names and financial instruments
    cols_to_match – columns to use for the matching process
    """
    firm_ner = replace_several_substrs(firm_ner)
    ## Compute matching scores and take the maximum per row (since a match may occur in one of several columns).
    dict_of_arrays_of_scores = {}
    for col in cols_to_match:
        dict_of_arrays_of_scores[col] = np.array([SequenceMatcher(None, firm_ner.upper(), replace_several_substrs(name).upper()).ratio() for name in df_ner_firms[col]]) 
    array_of_scores = np.array([array for array in dict_of_arrays_of_scores.values()])
    scores = np.max(array_of_scores, axis = 0)
    ## Find the row number of the matched entry in the reference table.
    index_found = np.argwhere(scores == np.amax(scores))
    index_found = [i[0] for i in index_found][0]

    res_dict = {'securityid': df_ner_firms.iloc[index_found, :]['securityid'], 'matching_score': np.take(scores, index_found)}
    return res_dict


### New one comparing to 2 NER
def find_and_filter_NERS(text, filter_value, df_ner_firms, nlp_rus) -> pd.DataFrame:
    """
    The function searches for named entities in the text using the spaCy library. Then, for each unique entity, it finds the most likely corresponding ticker.
    After that, it filters the matches based on confidence level.
    
    The output is a DataFrame with the following columns:
    text - the message text
    NER - the named entity found in the text
    ticker - the corresponding ticker
    
    Args:
    text – the input text to analyze
    filter_value – the confidence threshold for filtering ticker matches
    df_ner_firms – a reference table of company names and financial instruments
    nlp_rus – the Russian spaCy language model (e.g. from spacy.load('ru_core_news_lg'))
    """
    result = {'text': text, 'NER': [], 'ticker': []}
    ner_tikers = find_ner_firms(text, nlp_rus)
    if ner_tikers:
        ## Retain unique named entities only
        for ner in list(set(ner_tikers)):
            ## We map the extracted entities to our reference dataset
            potential = get_most_possible_firm(ner, df_ner_firms, cols_to_match = ['securityid', 'firm_name'])
            ## Keep only matches above a certain confidence level
            if potential['matching_score'] > filter_value:
                result['NER'].append(ner)   
                result['ticker'].append(potential['securityid'])       
    
    return pd.DataFrame(result)