import React, { Component } from 'react'
import GraphData from './GraphData';
import BoatInformation from './BoatInformation';
import ControlBoat from './ControlBoat';
import Recommender from './Recommender';

class App extends Component {
  render() {
    return (
      <div>
        <BoatInformation />
        <br />
        <GraphData  />
        <br />
        <ControlBoat />
        <br />
        <Recommender />        
      </div>
    )
  }
}

export default App;