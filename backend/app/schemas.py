from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


'''

project code

'''
#sentimment

class Sentiment(BaseModel):
    
    tweet_text: str
    sentiment: str
    score: float

    class Config:
        from_attributes = True

#similarities

class Similarity(BaseModel):
    text_in: str
    tweet_text: str
    sim_score: float

    class Config:
        from_attributes = True

# word_counts

class WordCountBase(BaseModel):
    word: str
    count: int
    


class WordCountCreate(WordCountBase):
    pass


class WordCount(WordCountBase):
    id: int

    class Config:
        from_attributes = True

# tweets

class TweetBase(BaseModel):
    #text: str
    text_clean: str
    author_id: int
    created_at: date


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int

    class Config:
        from_attributes = True

# authors

class AuthorBase(BaseModel):
    author_id: int

class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    tweets: list[Tweet] = []

    class Config:
        from_attributes = True