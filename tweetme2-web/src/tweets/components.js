import React from 'react'
import {useState, useEffect} from 'react';
import { apiTweetAction,
         apiTweetCreate, 
         apiTweetList } from './lookup';

export function TweetComponent(props) {
    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    const handleBackendUpdate = (response, status) => {
        let tempNewTweets = [...newTweets]
        if(status === 201) {
            tempNewTweets.unshift(response)
            setNewTweets(tempNewTweets)
        } else {
            console.log(response)
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newValue = textAreaRef.current.value
        apiTweetCreate(newValue, handleBackendUpdate)
        textAreaRef.current.value = ''
    }

    return <div className={props.className}>
        <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required='true' className="form-control" name='tweet'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
        </div>
        <TweetsList newTweets={newTweets} />
    </div>
}
  
export function TweetsList(props) {
    const [tweets, setTweets] = useState([])
    const [tweets2, setTweets2] = useState([])
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    console.log(props.newTweets)
    useEffect(() => {
        const final = [...props.newTweets].concat(tweets)
        if (final.length !== tweets2.length) {
            setTweets2(final)
        }
    }, [props.newTweets, tweets2, tweets])

    useEffect(() => {
        if (tweetsDidSet === false) {
            const handleTweetListLookup = (response, status) => {
                if (status === 200) {
                    setTweets(response)
                    setTweetsDidSet(true)
                } else {
                    alert("There was an error.")
                }
                }
                apiTweetList(handleTweetListLookup)   
        }
    }, [tweets, tweetsDidSet ,setTweetsDidSet])

    return tweets2.map((item, index) => {
        return <Tweet tweet={item} key={`${index}`} />
    })
}

export function ActionBtn(props) {
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
    // const [userLike, setUserLike] = useState(tweet.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary'
    const actionDisplay = action.display ? action.display : "Action"
    const handleActionBackendEvent = (response, status) => {
        if (status === 200) {
            setLikes(response.likes)
            // setUserLike(true)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiTweetAction(tweet.id, action.type, handleActionBackendEvent)
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
}
  
export function Tweet(props) {
    const {tweet} = props
    const className = props.className ? props.className : "my-5 py-5 border bg-white text-dark"
    return <div className={className}>
        <p>{tweet.id} - {tweet.content}</p>
        <div className='btn btn-group'>
        <ActionBtn tweet={tweet} action={{type: "like", display: "Likes"}} />
        <ActionBtn tweet={tweet} action={{type: "unlike", display: "Unlike"}} />
        <ActionBtn tweet={tweet} action={{type: "retweet", display: "Retweet"}} />
        </div>
    </div>
}
