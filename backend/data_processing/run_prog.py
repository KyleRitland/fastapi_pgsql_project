import pandas as pd
from .clean_data import clean_tweets, gen_clean_tweets_df, gen_clean_word_counts_df
from .export_data import export_dfs
from .generate_data import get_embeddings

def create_tweet_data():
    df = pd.read_json('17616581.tweets.jl', lines=True)
    document_df = pd.DataFrame(df['document'].to_list())
    document_df = document_df[document_df['lang'] == 'en'].copy()

    clean_tweets_sr = clean_tweets(document_df)
    embedding_list = get_embeddings(clean_tweets_sr)

    tweets_df = gen_clean_tweets_df(document_df, embedding_list, clean_tweets_sr)
    word_counts_df = gen_clean_word_counts_df(clean_tweets_sr)

    export_dfs(tweets_df, word_counts_df)