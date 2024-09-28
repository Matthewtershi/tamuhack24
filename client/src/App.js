import React, { useState, useEffect } from 'react';
import Hero from "./components/Hero.tsx";

import './index.css'

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/')  // Flask runs on port 5000 by default
      .then(response => response.json())
      .then(data => setData(data.message))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="bg-black-100 flex justify center items-center flex-col mx-auto px-5">
      <h1>{data ? data : "je mappelle cooked"}</h1>
      <Hero />
    </div>
  );
}

export default App;
