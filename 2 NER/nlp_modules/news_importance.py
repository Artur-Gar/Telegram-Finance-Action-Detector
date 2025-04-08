import numpy as np
from tqdm import tqdm

from nlp_modules.embeddinger import embed_bert_cls


def regress(text, regr, tokenizer, model):
    x = embed_bert_cls(text, tokenizer, model) 
    # print('emb', x, x.shape)
    return regr.predict(np.array([x]))

def regress_texts(texts, regr, tokenizer, model):
    predicts = []
    for text in tqdm(texts):
        res = regress(text, regr = regr, tokenizer = tokenizer, model = model)
        predicts.append(res[0])
    return predicts