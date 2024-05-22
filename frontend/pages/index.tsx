import React from "react";
import GeoMap from "../src/GeoMap";
import ButtonGroup from "../components/buttonGroup";

export default function Home() {

  

  return (
    <div className="App">
      <GeoMap />
      <div className="description ">
        <p className="mt-6 space-y-7 text-sm text-zinc-600 dark:text-zinc-400">
          <em>Grab simulator</em>
          &nbsp;is a simulation of the Grab ride-hailing service.<br /> It is
          developed by&nbsp; 
          <b>Bui Duy</b> <br />
        </p>
      </div>
        
      <ButtonGroup children={{}}/>
    </div>
  );
}
