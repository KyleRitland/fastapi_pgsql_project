import logo from './logo.svg';
import './App.css';

import Users from "./components/users.jsx";  // new
import TweetCountRange from './components/tweetsCountRange.jsx';
import TweetDateRange from './components/tweetsDateRange.jsx';

function App() {
  return (
    <div className="App">
    
      {/*<header className="App-header">*/}
      <header>
        
        {/*<img src={logo} className="App-logo" alt="logo" />*/}
        <h2>
          LinQuest tweet project
        </h2>
        {/*
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React 'This is extra text!'
        </a>
        */}
      </header>
      
      <Users />
      <TweetCountRange />
      <TweetDateRange />
      {/* <TweetDateRange /> */}
    </div>
    
  );
}

export default App;
