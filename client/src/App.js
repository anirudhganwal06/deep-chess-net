import React from "react";
import { BrowserRouter as Router, Route} from "react-router-dom";

import "./App.css";
import Landing from "./components/Layout/Landing";

function App() {
  return (
    <Router>
      <div className="App">
        <Route exact path="/" component={Landing} />
      </div>
    </Router>
  );
}

export default App;
