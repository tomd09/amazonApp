import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';
import { Item } from './components/item';

function App(){
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('All');
  const [amazonItems, setAmazonItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/selectionTypes');
        if (response.ok) {
          const result = await response.json();
          setSelectOptions(result);
        }
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [])

  const handleSelect = (e) => {
    setSelectedOption(e.target.value);
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/data?option=${encodeURIComponent(selectedOption)}`);
        if (response.ok) {
          const result = await response.json();
          setAmazonItems(result);
        }
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [selectedOption]);

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
          <p>Filter Items by Type</p>
          <select value={selectedOption} onChange={handleSelect}>
            {selectOptions.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
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