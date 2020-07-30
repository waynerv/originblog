import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {
  BrowserRouter as Router,
} from 'react-router-dom';
import CategroyStory from './stores/categroy';
import { Provider } from 'mobx-react'

ReactDOM.render(
  <Router >
    <Provider CategroyStory={CategroyStory}> 
      <App />
    </Provider>
  </Router>,
  document.getElementById('root')
);
