import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';
import { Item } from './components/item';

function App(){
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('All');
  const [amazonItems, setAmazonItems] = useState([]);
  const [fetchDataTrigger, setFetchDataTrigger] = useState(false);

  useEffect(() => {
    const fetchSelect = async () => {
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
    fetchSelect();
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
    if (fetchDataTrigger) {
      fetchData();
      setFetchDataTrigger(false);
    }
  }, [selectedOption, fetchDataTrigger]);

  const handleFormSubmit = async (formData) => {
    try {
      const response = await fetch('/addItem', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const result = await response.json();
        setFetchDataTrigger(true);
      } 
      } catch (error) {
        console.log(error);
      }
    }
  



  return (
    <div className="App">
      <header className="App-header">
        <h1>Amazon Web Scraper</h1>
      </header>
      <div className='container'>
        <div className='box itemDisplay'>
          <AddItemForm onFormSubmit={handleFormSubmit}/>
        </div>

        <div className='box itemSide'>
          <div className='typeSelection'>
            <p>Filter Items by Type</p>
            <select value={selectedOption} onChange={handleSelect}>
            {selectOptions.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
            </select>
          </div>

          <div className='itemList'>
            {amazonItems.map((item, index) => (
              <div key={index}>
                <Item item={item}/>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;