import './App.css';
import Home from './Home/home.tsx';
// import * as THREE from 'three'
import React, { useState, useEffect, useRef } from 'react'
// import TRUNK from 'vanta/dist/vanta.trunk.min'

function App() {
  // const [vantaEffect, setVantaEffect] = useState(null)
  // const myRef = useRef(null)
  
  // useEffect(() => {
  //   if (!vantaEffect) {
  //     setVantaEffect(TRUNK({
  //       el: myRef.current,
  //       THREE: THREE
  //     }))
  //   }
  //   return () => {
  //     if (vantaEffect) vantaEffect.destroy()
  //   }
  // }, [vantaEffect])

  return (
    <div 
    // ref={myRef}
    >
    <div className="App">
      <Home/>
    </div>
  </div>
  );
}

export default App;
