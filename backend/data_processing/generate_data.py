import pandas as pd
import random
import torch
from transformers import BertTokenizer, BertModel

"""
pytorch with CUDA enabled installed with followinf command for windows 11

py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

"""

def get_embeddings(clean_tweets_in):

    print('...........start get_embeddings()........')

    # check that pytorch is running and can access GPU

    print(torch.cuda.__spec__)
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_capability())
    print(torch.cuda.get_arch_list())
    print(torch.cuda.is_available())

    # set random seed for reproducability

    random_seed = 42
    random.seed(random_seed)
    
    torch.manual_seed(random_seed)
    if torch.cuda.is_available():
        print('torch cuda is available. settings seed.....')
        torch.cuda.manual_seed_all(random_seed)
        print('seed set........')
    else:
        print('cuda NOT available')
        exit()

    print('...........making tokenizer and model........')

    # use pretrained english language BERT tokenizer and model

    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')

    # connect BERT model to GPU

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    bert_model.to(device)

    print('........... tokenizer and model made........')
    
    print('...........making tokenizer........')

    bert_encoding = bert_tokenizer.batch_encode_plus(
        clean_tweets_in.values,                    # List of input texts
        padding=True,              # Pad to the maximum sequence length
        truncation=True,           # Truncate to the maximum sequence length if necessary
        return_tensors='pt',      # Return PyTorch tensors
        add_special_tokens=True    # Add special tokens CLS and SEP
    )

    # connect BERT encoder data to GPU

    for k, v in bert_encoding.items():
        bert_encoding[k] = v.to(device)

    print('........... tokenizer made........')
    input_ids = bert_encoding['input_ids']  # Token IDs
    
    attention_mask = bert_encoding['attention_mask']  # Attention mask
    
    print('...........making embeddings........')

    # feed ids and masks into model to generate embeddings

    with torch.no_grad():
        outputs = bert_model(input_ids, attention_mask=attention_mask)

        #retrieve context aware word embeddings
        word_embeddings = outputs.last_hidden_state

    # perform average pooling along the sequence length dimension

    sentence_embedding = word_embeddings.mean(dim=1)

    print('........... embeddings made........')

    # convert embeddings into list of strings for input into PostGreSQL tables

    embedding_list = list(map(str, sentence_embedding.tolist()))
    embedding_list = [i.replace('[', '{').replace(']', '}') for i in embedding_list]

    print('...........end get_embeddings()........')

    return embedding_list
