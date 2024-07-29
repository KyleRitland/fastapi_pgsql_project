import itertools
import re
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from collections import Counter

def gen_clean_word_counts_df(clean_tweets_in):
    
    def remove_extra(text):
            return text.strip().replace("\n", "").replace(",", "").replace('""', '"')
        
    stop_words = set(stopwords.words('english'))
    stop_words = {s.replace("'", "") for s in stop_words}
    print(stop_words)
    def remove_stop_words(tweet_in):
 
        word_tokens = word_tokenize(tweet_in.lower())
        filtered_sentence = ' '.join([w for w in word_tokens if (w not in stop_words) and (w != 'rt')])
        
        return remove_extra(re.sub('[^a-z A-Z 0-9]+', '', filtered_sentence))

    
    all_words = Counter(' '.join([remove_stop_words(item) for item in clean_tweets_in]).split(' '))
    keys = all_words.keys()
    values = all_words.values()

    word_counts_df = pd.DataFrame({'words': keys, 'counts': values})
    word_counts_df.insert(0, "id", [i for i in range(word_counts_df.shape[0])], True)

    return word_counts_df

def gen_clean_tweets_df(df_in, embedding_list_in, clean_tweets_in):
    tweets_df = df_in[['id', 'created_at']].copy()
    
    datetime_df = pd.DataFrame(data=pd.to_datetime(tweets_df['created_at']).dt.strftime('%Y-%m-%d'), columns=['created_at'])
    
    tweets_df.update(datetime_df)
    
    tweets_df.rename(columns={'id': 'author_id'}, inplace=True)
    tweets_df.insert(0, "id", [i for i in range(tweets_df.shape[0])], True)

    tweets_df.insert(0, 'embedding', embedding_list_in)

    tweets_df.insert(0, "text_clean", clean_tweets_in, True)
    
    tweets_df = tweets_df.copy()[['id', 'author_id', 'created_at', 'text_clean', 'embedding']]
    #tweets_df.update(pt_df)
    #print(clean_tweets_sample.shape)
    # tweets_df[]
    print(tweets_df.columns)
    print(tweets_df.info())

    return tweets_df

def clean_tweets(df_in):
    return df_in.apply(lambda row: clean_tweet_text(row), axis=1)


def clean_tweet_text(tweet_data):
    tweet = tweet_data['text']
    range_list = []
    indices = [True] * len(tweet)
    # print(tweet_data)

    range_list = ([i['indices'] for i in tweet_data['entities']['user_mentions']] + 
                  [i['indices'] for i in tweet_data['entities']['urls']] + 
                  [i['indices'] for i in tweet_data['entities']['hashtags']])
    
    keys = tweet_data['entities'].keys()
    if 'media' in keys:
        if tweet_data['entities']['media'] is not None:
            range_list = range_list + [med['indices'] for med in tweet_data['entities']['media']]

    # print(range_list)

    for start_idx, end_idx in range_list:
        for i in range(start_idx - 1, end_idx):
            indices[i] = False

    res = ''.join(itertools.compress(tweet, indices))
    # print(res)
    tweet = res.lower()
    # print(tweet)
    # tweet = re.sub('@[^\s]+','', tweet)
    tweet = re.sub('[^a-z A-Z 0-9]+', '', tweet).strip()
    tweet = tweet.replace("\n", "")
    return tweet
