from transformers import AutoTokenizer, AutoModel
import torch

def embed_bert_cls(text: str, tokenizer: AutoTokenizer,
                    model: AutoModel) -> torch.Tensor:
    """
    The function takes a text and returns its embedding
    Args:
    text – the input text
    tokenizer – the tokenizer for the text
    model – the encoder model used to generate embeddings (typically BERT)
    """
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return torch.Tensor(embeddings[0].cpu().numpy()) 
    


