import React from 'react'
import {useState, useEffect} from 'react';
import { loadTweets } from '../lookup';

export function TweetComponent(props) {
    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    const handleSubmit = (event) => {
        event.preventDefault()
        const newValue = textAreaRef.current.value
        let tempNewTweets = [...newTweets]
        tempNewTweets.unshift({
            content: newValue,
            likes: 0,
            id: 12313
        })
        setNewTweets(tempNewTweets)
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
    console.log(props.newTweets)
    useEffect(() => {
        const final = [...props.newTweets].concat(tweets)
        if (final.length !== tweets2.length) {
            setTweets2(final)
        }
    }, [props.newTweets, tweets2, tweets])

    useEffect(() => {
        const myCallback = (response, status) => {
        if (status === 200) {
            setTweets(response)
        } else {
            alert("There was an error.")
        }
        }
        loadTweets(myCallback)
    }, [])

    return tweets2.map((item, index) => {
        return <Tweet tweet={item} key={`${index}`} />
    })
}

export function ActionBtn(props) {
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
    const [userLike, setUserLike] = useState(tweet.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary'
    const actionDisplay = action.display ? action.display : "Action"
    const handleClick = (event) => {
        event.preventDefault()
        if (action.type === 'like') {
            if (userLike === true) {
                setLikes(likes - 1)
                setUserLike(false)
            }
            else {
                setLikes(tweet.likes + 1)
                setUserLike(true)
            }
        } 
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
        {/* <ActionBtn tweet={tweet} action={{type: "unlike", display: "Unlike"}} /> */}
        <ActionBtn tweet={tweet} action={{type: "retweet", display: "Retweet"}} />
        </div>
    </div>
}
