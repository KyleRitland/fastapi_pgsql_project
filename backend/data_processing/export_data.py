import pandas as pd

def export_dfs(tweets_df_in, word_counts_df_in):
    
    word_counts_df_in.to_csv('word_counts_df.csv', index=False)
    tweets_df_in.to_csv('tweets_df.csv', index=False)
    