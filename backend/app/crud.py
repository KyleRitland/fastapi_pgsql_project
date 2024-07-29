from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()


'''

project code

'''


from collections import Counter
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from transformers import BertTokenizer, BertModel
import torch

def get_tweet_sim(db: Session, text_in: str = "", limit: int = 0):
    print(f'text_in: {text_in}')
    db.execute("""SELECT * FROM tweets""")
    tweets_all = db.fetchall()

    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')

    example_encoding = bert_tokenizer.batch_encode_plus(
        [text_in],
        padding=True,
        truncation=True,
        return_tensors='pt',
        add_special_tokens=True
    )
    example_input_ids = example_encoding['input_ids']
    example_attention_mask = example_encoding['attention_mask']
    
    # Generate embeddings for the example sentence
    with torch.no_grad():
        example_outputs = bert_model(example_input_ids, attention_mask=example_attention_mask)
        example_sentence_embedding = example_outputs.last_hidden_state.mean(dim=1)

    #cos_sim = sorted(cosine_similarity(torch.Tensor([i[4] for i in tweets_all]), example_sentence_embedding), reverse=True)[:limit]
    cos_sim = cosine_similarity(torch.Tensor([i[4] for i in tweets_all]), example_sentence_embedding)
    print(tweets_all[0][3])
    print(cos_sim[0])
    zip_group = [[tweets_all[i][3], cos_sim[i][0]] for i in range(len(cos_sim))]
    zip_group = sorted(zip_group, key=lambda x: x[1], reverse=True)[:limit]
    print('zip_group', zip_group)
    #test_g = zip(tweets_all[:limit], cos_sim)
    '''for item in test_g:
        print(item)'''
    tweets_sim = [schemas.Similarity( text_in=text_in, tweet_text=item[0], sim_score=item[1]) for item in zip_group]
    print('tweets_keyword',tweets_sim)
    '''for i in tweets_all[:10]:
        print()
        print(type(torch.Tensor(i[4])), type(example_sentence_embedding))
        
        print(cos_sim)
        #print(i[4])
        print()'''
    return tweets_sim

def get_tweets_top_n(db: Session, top_n_words: int = 5):
    db.execute(
        """SELECT * FROM word_counts ORDER BY count DESC LIMIT %s""",
        (top_n_words, ))
    all_words = db.fetchall()
    all_words = [schemas.WordCount(id=item[0], word=item[1], count=item[2]) for item in all_words]
    
    return all_words
def get_tweets_keyword(db: Session, keyword: str = "keyword"):
    
    tweets_keyword = db.fetchall()
    tweets_keyword = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2], text_clean=item[3]) for item in tweets_keyword]
    
    return tweets_keyword

def get_tweets_dr(db: Session, start_dt: str, end_dt: str):
    print(f'get_tweets_dr() - start_dt: {start_dt} - type {type(start_dt)}, end_dt: {end_dt} - type {type(end_dt)}')
    
    db.execute(
        """SELECT * FROM tweets WHERE created_at BETWEEN %s AND %s""",
        (start_dt, end_dt,)
        )
    tweets_dr = db.fetchall()
    #print('............ start test ........')
    #print(type(tweets_dr[0]))
    #tweets_dr = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2].strftime('%Y-%m-%d'), text_clean=item[3]) for item in tweets_dr]
    tweets_dr = [schemas.Tweet(id=item[0], author_id=item[1], created_at=item[2], text_clean=item[3]) for item in tweets_dr]
        
    #for i in tweets_dr:
    #    print(i)
    #print('............ end test ........')
    
    return tweets_dr
    #return db.query(models.Tweet).filter(models.Tweet.created_at >= start_dt).all()


