from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from nlp_modules.embeddinger import embed_bert_cls

def find_text_similarity(text_1: str, text_2: str, tokenizer: AutoTokenizer,
                    model: AutoModel) -> float:
    """
    The function computes embeddings for two texts and, based on the chosen metric, returns a similarity score (using cosine similarity by default)
    Args:
    text_1 – the first text to compare
    text_2 – the second text to compare
    tokenizer – the tokenizer for the texts
    model – the encoder model used to generate embeddings (typically BERT)
    """
    emb_1 = embed_bert_cls(text_1, tokenizer = tokenizer, model = model)
    emb_2 = embed_bert_cls(text_2, tokenizer = tokenizer, model = model)
    cosine = cosine_similarity(emb_1.reshape(1, -1), emb_2.reshape(1, -1))
    return cosine[0][0]