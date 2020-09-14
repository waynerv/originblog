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
const Categroy =lazy(()=> import('./components/Categroy'))
const Update =lazy(()=> import('./components/Update'))
const Article =lazy(()=> import('./components/View'))

function Home() {
  return (
    <>
      <Nav/>
      <main>
        <Suspense fallback={<div>Loading!!</div>}>
          <Switch>
            <Route path='/view/editor' component={Editor} />
            <Route path='/view/categroy' component={Categroy} />
            <Route path='/view/history' component={History} />
            <Route path='/view/update' component={Update} />
            <Route path='/view/information' component={Information} />
            <Route path='/view/article' component={Article} />
            <Redirect from='/view' to='/view/history'/>
          </Switch>
        </Suspense> 
      </main>
    </>
  )
}

export default Home;
