
export function TweetDisplay({tweets,}) {
    console.log('tweets')
    console.log(tweets)
    if (tweets) {
        const TweetsTable = tweets.map(
        (
            { id, text, text_clean }, 
            index,
        ) => (
            <div key={id} position={index}>
                <div style={{textAlign: 'left', paddingLeft: 50, paddingRight: 50}}>
                    <p>
                        <span><b>Tweet {id}:</b></span>
                        <br/>
                        <span style={{paddingLeft: 50}}><b>Raw text:</b> {text}</span>
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