import React, { Component } from 'react'
import GraphData from './GraphData';
import BoatInformation from './BoatInformation';
import ControlBoat from './ControlBoat';

class App extends Component {
  render() {
    return (
      <div>
        <BoatInformation />
        <br />
        <GraphData  />
        <br />
        <ControlBoat />
      </div>
    )
  }
}

export default App;