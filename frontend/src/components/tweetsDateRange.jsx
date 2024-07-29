import React, { useEffect, useState } from "react";
import { TweetDisplayDateRange } from './general_comp.jsx'

const TweetsDateRangeContext = React.createContext({
    TweetRange: [], fetchTweetRange: () => {}
})

export default function TweetDateRange() {
  const [tweetRange, setTweetRange] = useState([])
  const [start_dt, setStart_dt] = useState('2018-01-01');
  const [end_dt, setEnd_dt] = useState('2018-01-22');

  const fetchTweetRange = async () => {
    const response = await fetch(`http://localhost:8000/tweets/date_range/?start_dt=${start_dt}&end_dt=${end_dt}`)
    const tweet_range = await response.json()
    console.log('tweet_range')
    console.log(tweet_range)
    setTweetRange(tweet_range)
  }

  function onStartDtChange(evt) {
    setStart_dt(evt.target.value);
  }

  function onEndDtChange(evt) {
    setEnd_dt(evt.target.value);
  }

  return (
    <TweetsDateRangeContext.Provider value={{tweetRange, fetchTweetRange}}>
        <div>
        <div><span style={{paddingRight: 10}}>Start date:</span><input type="date" id="start_datetime" name="start_datetime" value={start_dt} onChange={onStartDtChange}></input></div>
        <div><span style={{paddingRight: 10}}>End date:</span><input type="date" id="end_datetime" name="end_datetime" value={end_dt} onChange={onEndDtChange}></input></div>
        </div>
        <br/>
        <button type="button" onClick={fetchTweetRange}>Get tweets in datetime range</button>
        {tweetRange?
            TweetDisplayDateRange({tweetRange})
        : <div>No tweets</div>}
    </TweetsDateRangeContext.Provider>
  )
}