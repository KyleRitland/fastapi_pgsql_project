from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import types
from sqlalchemy.orm import Session

from . import crud, schemas
#from database import SessionLocal, engine

from .db_config import create_connection


from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import pandas as pd

from ..data_processing.run_prog import create_tweet_data

#create_tweet_data() #run code to generate data for PostGreSQL database

DB_connection = create_connection()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend URL
@app.get("/")
def index():
    return FileResponse("frontend/src/App.js")

@app.exception_handler(404)
def exception_404_handler(request, exc):
    return FileResponse("frontend/src/App.js")

#app.mount("/", StaticFiles(directory="frontend/src/"), name="ui")

#Base.metadata.create_all(bind=engine)

# Dependency

def get_db():
    db = DB_connection.cursor()
    print('getting db........')
    try:
        yield db
    finally:
        db.close()

@app.get("/tweets/", response_model=list[schemas.Tweet])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tweets = crud.get_tweets(db, skip=skip, limit=limit)
    return tweets

'''

project code

'''

@app.get("/tweets/calculate_sim/", response_model=list[schemas.Similarity])
def get_similarities(text_in: str, limit: int, db: Session = Depends(get_db)):
    print(f'text_in: {text_in} - type {type(text_in)}')
    if isinstance(text_in, str):
        print('text_in is a string')
        tweets_sim = crud.get_tweet_sim(db, text_in=text_in, limit=limit)
    if tweets_sim is None:
        raise HTTPException(status_code=404, detail="No tweets in date range found")
    
    return tweets_sim

@app.get("/tweets/top_n/", response_model=list[schemas.WordCount])
def get_top_N(top_n_words: int, db: Session = Depends(get_db)):
    if isinstance(top_n_words, int):
        tweets_top_n = crud.get_tweets_top_n(db, top_n_words=top_n_words)
    if tweets_top_n is None:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets_top_n

@app.get("/tweets/keyword/", response_model=list[schemas.Tweet])
def get_tweets_by_keyword(keyword: str, db: Session = Depends(get_db)):
    if isinstance(keyword, str):
        tweets_keyword = crud.get_tweets_keyword(db, keyword=keyword)
    if tweets_keyword is None:
        raise HTTPException(status_code=404, detail="No tweets with keyword found")
    return tweets_keyword

@app.get("/tweets/date_range/", response_model=list[schemas.Tweet])
def get_tweets_by_date(start_dt: str, end_dt: str, db: Session = Depends(get_db)):
    print(f'start_dt: {start_dt} - type {type(start_dt)}, end_dt: {end_dt} - type {type(end_dt)}')
    if isinstance(start_dt, str) and isinstance(end_dt, str):
        print('both start and end dt are strings')
        if pd.to_datetime(start_dt)<=pd.to_datetime(end_dt):
            tweets_dr = crud.get_tweets_dr(db, start_dt=start_dt, end_dt=end_dt)
        else:
            raise HTTPException(status_code=400, detail="end date is earlier than start date")
    #else:
        #raise HTTPException(status_code=400, detail="parameters given not strings")
        
    if tweets_dr is None:
        raise HTTPException(status_code=404, detail="No tweets in date range found")
    
    return tweets_dr