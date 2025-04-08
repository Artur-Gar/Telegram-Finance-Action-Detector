import pandas as pd
from difflib import SequenceMatcher
import numpy as np

from nlp_modules.general_string_helpers import replace_several_substrs

def get_most_possible_firm(firm_ner: str, df_ner_firms: pd.DataFrame, cols_to_match: list = ['firm_name']) -> dict:
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