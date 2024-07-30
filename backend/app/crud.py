from sqlalchemy.orm import Session

from . import schemas

from sklearn.metrics.pairwise import cosine_similarity

import torch
from transformers import BertTokenizer, BertModel

import re

'''

testing tweet retrival from table + database

'''

def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    db.execute(
        """SELECT * FROM tweets ORDER BY created_at ASC LIMIT %s OFFSET %s""",
        (limit, skip))
    tweets_retrieved = db.fetchall()
    tweets_retrieved = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2], text_clean=item[3]) for item in tweets_retrieved]
    
    return tweets_retrieved


'''

main project code

'''
from transformers import pipeline
SentimentClassifier = pipeline("sentiment-analysis")

def get_sentiments_by_text_in(text_in: str):

    sent = SentimentClassifier(text_in)

    return [schemas.Sentiment(tweet_text=text_in, sentiment=sent[0]['label'], score=sent[0]['score'])]

def get_sentiments_by_date(db: Session, start_dt: str, end_dt: str):

    db.execute(
        """SELECT * FROM tweets WHERE created_at BETWEEN %s AND %s""",
        (start_dt, end_dt,)
        )
    
    tweets_to_get_sentiment = db.fetchall()
    just_tweets = [item[3] for item in tweets_to_get_sentiment]
    sent = SentimentClassifier(just_tweets)
    sent_f = [(just_tweets[i], sent[i]['label'], sent[i]['score']) for i in range(len(sent))]
    
    return [schemas.Sentiment(tweet_text=item[0], sentiment=item[1], score=item[2]) for item in sent_f]

def get_tweet_sim(db: Session, text_in: str = "", limit: int = 0):
    print(f'text_in: {text_in}')
    db.execute("""SELECT * FROM tweets""")
    tweets_all = db.fetchall()

    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')

    #create encoder for text from user
    text_in_encoding = bert_tokenizer.batch_encode_plus(
        [text_in],
        padding=True,
        truncation=True,
        return_tensors='pt',
        add_special_tokens=True
    )
    text_in_input_ids = text_in_encoding['input_ids']
    text_in_attention_mask = text_in_encoding['attention_mask']
    
    # Generate embedding
    with torch.no_grad():
        example_outputs = bert_model(text_in_input_ids, attention_mask=text_in_attention_mask)
        example_sentence_embedding = example_outputs.last_hidden_state.mean(dim=1)

    #calculate cosine simmilarity between input text embedding and tweet embeddings
    
    cos_sim = cosine_similarity(torch.Tensor([i[4] for i in tweets_all]), example_sentence_embedding)
    
    #combign tweet text and sim score in one list,
    # then sort tweets by similarity score to input text and retrieve top N scoring tweets

    zip_group = [[tweets_all[i][3], cos_sim[i][0]] for i in range(len(cos_sim))]
    zip_group = sorted(zip_group, key=lambda x: x[1], reverse=True)[:limit]
    
    #create list of schema for FastAPI return
    tweets_sim = [schemas.Similarity( text_in=text_in, tweet_text=item[0], sim_score=item[1]) for item in zip_group]
    
    return tweets_sim

def get_tweets_top_n(db: Session, top_n_words: int = 5):
    db.execute(
        """SELECT * FROM word_counts ORDER BY count DESC LIMIT %s""",
        (top_n_words, ))
    all_words = db.fetchall()
    all_words = [schemas.WordCount(id=item[0], word=item[1], count=item[2]) for item in all_words]
    
    return all_words

def get_tweets_keyword(db: Session, keyword: str = "keyword"):
    
    kw_claen = re.sub('[^a-z A-Z 0-9]+', '', keyword).strip()
    db.execute(f"SELECT id, author_id, created_at, text_clean FROM tweets WHERE text_clean ILIKE '%{kw_claen}%'")
    
    tweets_keyword = db.fetchall()
    print(tweets_keyword)
    tweets_keyword = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2], text_clean=item[3]) for item in tweets_keyword]
    
    return tweets_keyword

def get_tweets_dr(db: Session, start_dt: str, end_dt: str):
    print(f'get_tweets_dr() - start_dt: {start_dt} - type {type(start_dt)}, end_dt: {end_dt} - type {type(end_dt)}')
    
    db.execute(
        """SELECT * FROM tweets WHERE created_at BETWEEN %s AND %s""",
        (start_dt, end_dt,)
        )
    tweets_dr = db.fetchall()
    tweets_dr = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2], text_clean=item[3]) for item in tweets_dr]
        
    return tweets_dr
    

