import React, { useState, useEffect } from 'react';
import './App.css'

function App(){
  const [data, setData] = useState({
    name: '',
    age: '',
    date: '',
    programming: ''
  });

  useEffect(() => {
    fetch('/data').then((res) => 
      res.json().then((data) => {
        setData({
          name: data.Name,
          age: data.Age,
          date: data.Date,
          programming: data.Programming
        });
      })
    );
  }, []);

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Flask and React</h1>
        <p>{data.name}</p>
        <p>{data.age}</p>
        <p>{data.date}</p>
        <p>{data.programming}</p>
      </header>
    </div>
  );
}

export default App;