import React from 'react';
import {
  Switch,
  Route
} from 'react-router-dom';
import Login from './pages/login';
import Home from './home';



function App() {
  return (
    <>
      <Switch>
        <Route path='/' exact component={Login} />
        <Route path='/view' component={Home} >
        </Route>
      </Switch>
</>
  )
}

export default App;
