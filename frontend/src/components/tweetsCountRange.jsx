import React, { useEffect, useState } from "react";
import { TweetDisplay } from './general_comp.jsx'

const TweetsCountRangeContext = React.createContext({
    tweets: [], fetchTweets: () => {}
})

export default function TweetCountRange() {
    const [tweets, setTweets] = useState([])
    const [skip, setSkip] = useState('0');
    const [limit, setLimit] = useState('10');
  
    const fetchTweets = async () => {
      const response = await fetch(`http://localhost:8000/tweets/?skip=${skip}&limit=${limit}`)
      const tweets = await response.json()
      console.log('tweets')
      console.log(tweets)
      setTweets(tweets)
    }
  
  function onSkipChange(evt) {
    setSkip(evt.target.value);
  }

  function onLimitChange(evt) {
    setLimit(evt.target.value);
  }

  return (
    <TweetsCountRangeContext.Provider value={{tweets, fetchTweets}}>
        <input type="text" placeholder="Set skip" value={skip} onChange={onSkipChange} />
        <input type="text" placeholder="Set limit" value={limit} onChange={onLimitChange} />
        <button type="button" onClick={fetchTweets}>Get tweets</button>
        <p><b>Skip value:</b> {skip}, <b>Limit value:</b> {limit}</p>
            <p><b>Tweets:</b></p>
        {tweets?
            TweetDisplay({tweets})
        : <div>No tweets</div>}
    </TweetsCountRangeContext.Provider>
  )
}