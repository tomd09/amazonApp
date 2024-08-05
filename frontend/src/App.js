import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';
import { Item } from './components/item';

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
        <h1>Amazon Web Scraper</h1>
      </header>
      <div className='container'>
        <div className='box itemDisplay'>
          <AddItemForm />
        </div>
        <div className='box itemList'>
          <ul>
            {amazonItems.map((item, index) => (
              <div key={index}>
                <Item item={item}/>
                <br/>
              </div>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;