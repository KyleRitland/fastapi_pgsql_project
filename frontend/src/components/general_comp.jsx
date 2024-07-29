
export function TweetDisplay({tweets,}) {
    console.log('tweets')
    console.log(tweets)
    if (tweets) {
        const TweetsTable = tweets.map(
        (
            { id, author_id, created_at, text_clean }, 
            index,
        ) => (
            <div key={id} position={index}>
                <div style={{textAlign: 'left', paddingLeft: 50, paddingRight: 50}}>
                    <p>
                        <span><b>Tweet {id}:</b></span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>author ID:</b> {author_id}</span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>Date created:</b> {created_at}</span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>Cleaned text:</b> {text_clean}</span>
                    </p><hr></hr>
                </div>
            </div>
        )
    )

    return (
        <>
        {TweetsTable}
        </>
    );
} else {
    return (
        <>
        <p>No tweets selected yet</p>
        </>
    );
}
    
}

export function TweetDisplayDateRange({tweetRange,}) {
    console.log('tweetRange')
    console.log(tweetRange)
    if (tweetRange) {
        const TweetsTable = tweetRange.map(
        (
            { id, author_id, created_at, text_clean }, 
            index,
        ) => (
            <div key={id} position={index}>
                <div style={{textAlign: 'left', paddingLeft: 50, paddingRight: 50}}>
                    <p>
                        <span><b>Tweet {id}:</b></span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>author ID:</b> {author_id}</span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>Date created:</b> {created_at}</span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>Cleaned text:</b> {text_clean}</span>
                    </p><hr></hr>
                </div>
            </div>
        )
    )

    return (
        <>
        {TweetsTable}
        </>
    );
} else {
    return (
        <>
        <p>No tweets selected yet</p>
        </>
    );
}
    
}