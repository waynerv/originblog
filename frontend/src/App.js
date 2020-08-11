import React, {lazy , Suspense} from 'react';
import Footer from './components/footer';
import {
  Switch,
  Route
} from 'react-router-dom';

const Home = lazy(() => import('./pages/home'));
const History =lazy(() => import('./pages/history'));
const About =lazy(() => import('./pages/about'));

function App() {
  return (
    <>
    <Suspense fallback={<p>Loading!</p>}>
      <Switch>
        <Route path='/' exact component={Home} />
        <Route path='/history' component={History} />
        <Route path='/about' component={About} />
      </Switch>
    </Suspense>
      <Footer />
    </>
  );
}

export default App;
