import pandas as pd
import yaml
from langchain.chat_models.gigachat import GigaChat
import spacy

from ners_and_calls_modules.identify_ners import find_and_filter_NERS 
from ners_and_calls_modules.find_call.kor_llm import call_determination 

## configs and LLM
config_path = r"configs\config.yml" 
with open(config_path) as fh:
    read_config = yaml.load(fh, Loader=yaml.FullLoader)
creds = read_config['creds']
model = read_config['model']
filter_value = read_config['filter_value']
df_ner_firms_PATH = read_config['df_ner_firms_PATH']

llm = GigaChat(
    credentials = creds, 
    verify_ssl_certs = False, 
    model = model, 
    scope = "GIGACHAT_API_CORP", 
    profanity_check = 'false', 
    temperature = 0.5, 
    max_tokens = 30
    )

## A refernce table for company names and tickers
df_ner_firms = pd.read_excel(df_ner_firms_PATH)
## spacy_model
nlp_rus = spacy.load('ru_core_news_lg')

def get_ners_and_calls(text: str, filter_value: float) -> pd.DataFrame:
    """
    The function returns a DataFrame with the following columns:
    text - the message text
    NER - the named entity found in the text
    ticker - the corresponding ticker
    call - whether there is a call to action (1) or not (0)

    Args:
    text – the text to be analyzed
    filter_value – the confidence threshold for filtering tickers
    """
    final_df = find_and_filter_NERS(text, filter_value = filter_value, df_ner_firms = df_ner_firms, nlp_rus=nlp_rus)
    calls = []
    print(llm)
    for i in range(final_df.shape[0]):
        ner = final_df.loc[i, 'NER']
        ticker = final_df.loc[i, 'ticker']
        text = final_df.loc[i, 'text']
        calls.append(call_determination(text, ner, ticker, llm))
    final_df['call'] = calls
    
    return final_df



