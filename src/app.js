import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import Home from './home'
import UploadForm from './uploadForm'
import Upload from './upload'

export default function App() {
  return (<React.StrictMode>
    <Router>
      <div>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route exact path="/upload">
            <UploadForm />
          </Route>
          <Route exact path="/uploads/:id">
            <Upload />
          </Route>
        </Switch>
      </div>
    </Router>
  </React.StrictMode>)}