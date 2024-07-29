import React, { useEffect, useState } from "react";

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

    /*
  useEffect(() => {
    

    if (skip && limit) {
        fetchUsers(skip, limit);
    }
    //fetchUsers()
  }, [skip, limit])
    */
  
  

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
        {/*
        <input type="text" placeholder="Set start datetime" value={start_dt} onChange={onStartDtChange} />
        <input type="text" placeholder="Set end datetime" value={end_dt} onChange={onEndDtChange} />
        */}
        <br/>
        <button type="button" onClick={fetchTweetRange}>Get tweets in datetime range</button>
        {tweetRange?
          <div>
            <p>Start date read: {start_dt}, End date read: {end_dt}</p>
            <p>Tweets:</p>
            {tweetRange.map((tweet) => (
           <li key={tweet.id}><p>Tweet date: {tweet.created_at}</p><p>Raw text: {tweet.text}</p><p>Cleaned text: {tweet.text_clean}</p><br/></li>
         ))}
         </div>
        : <div>No tweets found in date range</div>}
    </TweetsDateRangeContext.Provider>
  )
}