import itertools
import re
from nltk.corpus import stopwords

def clean_tweet_text_2(tweet_data):
        
        tweet = tweet_data['text']
        range_list = []
        indices = [True] * len(tweet)
        #print(tweet_data)

        '''
        #print(user_mentions)
        for m in tweet_data['entities']['user_mentions']:

            #print(m['indices'])
            #print(tweet[:m['indices'][0]] + tweet[m['indices'][1]:])
            #tweet = tweet[:m['indices'][0]] + tweet[m['indices'][1]:]
            range_list.append(m['indices'])

        for url in tweet_data['entities']['urls']:
            # print(m['indices'])
            # print(tweet[:m['indices'][0]] + tweet[m['indices'][1]:])
            #tweet = tweet[:url['indices'][0]] + tweet[url['indices'][1]:]
            range_list.append(url['indices'])

        for ht in tweet_data['entities']['hashtags']:
            # print(m['indices'])
            # print(tweet[:m['indices'][0]] + tweet[m['indices'][1]:])
            #tweet = tweet[:ht['indices'][0]] + tweet[ht['indices'][1]:]
            range_list.append(ht['indices'])

        if tweet_data['entities']['media'] is not None:
            for med in tweet_data['entities']['media']:
                # print(m['indices'])
                # print(tweet[:m['indices'][0]] + tweet[m['indices'][1]:])
                #print('media: ', med['indices'][0], med['indices'][1], tweet[med['indices'][0]], tweet[med['indices'][1]], tweet[med['indices'][0]:med['indices'][1]])
                #tweet = tweet[:med['indices'][0]] + tweet[med['indices'][1]:]
                range_list.append(med['indices'])
        '''

        range_list = [i['indices'] for i in tweet_data['entities']['user_mentions']] + [i['indices'] for i in
                                                                                        tweet_data['entities'][
                                                                                            'urls']] + [i['indices'] for
                                                                                                        i in tweet_data[
                                                                                                            'entities'][
                                                                                                            'hashtags']]
        keys = tweet_data['entities'].keys()
        if 'media' in keys:
            if tweet_data['entities']['media'] is not None:
                range_list = range_list + [med['indices'] for med in tweet_data['entities']['media']]

        #print(range_list)

        for start_idx, end_idx in range_list:
            for i in range(start_idx - 1, end_idx):
                indices[i] = False

        res = ''.join(itertools.compress(tweet, indices))
        # print(res)
        tweet = res.lower()
        # print(tweet)
        # tweet = re.sub('@[^\s]+','', tweet)
        tweet = re.sub('[^a-z A-Z 0-9]+', '', tweet)
        # print(tweet)
        
        return tweet