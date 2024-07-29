import logo from './logo.svg';
import './App.css';

import TweetCountRange from './components/tweetsCountRange.jsx';
import TweetDateRange from './components/tweetsDateRange.jsx';

function App() {
  return (
    <div className="App">
    
      <header>
        
        <h2>
          FastAPI - PostGreSQL - React.js - tweet project
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
      
      <TweetCountRange />
      <TweetDateRange />
    </div>
    
  );
}

export default App;
