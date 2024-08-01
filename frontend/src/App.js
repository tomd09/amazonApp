import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';

function App(){
  const [amazonItems, setAmazonItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/data');
        if (response.ok) {
          const result = await response.json();
          setAmazonItems(result);
        }
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Flask and React</h1>
      </header>
      <div>
            {amazonItems.map((item, index) => (
                <div key={index}>
                    <p>Name: {item.Name}</p>
                    <p>Type: {item.Type}</p>
                    <p>Price: {item.Price}</p> 
                    <p>Time: {item.Time}</p>
                </div>
            ))}
        </div>
        <AddItemForm />
    </div>
  );
}

export default App;