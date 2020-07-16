import React, {lazy, Suspense} from 'react';
import {
  Switch,
  Route,
  Redirect
} from 'react-router-dom';
import Nav from './components/nav';
import './index.css';
import History from './components/History';
const Editor = lazy(()=> import('./components/Editor'));
const Information = lazy(()=> import('./components/Information'));

function Home() {
  return (
    <>
      <Nav/>
      <main>
        <Suspense fallback={<div>Loading!!</div>}>
          <Switch>
            <Route path='/view/editor' component={Editor} />
            <Route path='/view/history' component={History} />
            <Route path='/view/information' component={Information} />
            <Redirect from='/view' to='/view/history'/>
          </Switch>
        </Suspense> 
      </main>
    </>
  )
}

export default Home;
