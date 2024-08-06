import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';
import {Item } from './components/item';

function App(){
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('All');
  const [amazonItems, setAmazonItems] = useState([]);
  const [fetchDataTrigger, setFetchDataTrigger] = useState(false);
  const [itemData, setItemData] = useState('')

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
          setItemData(result[0].Name);
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
        console.log(result);
        setFetchDataTrigger(true);
      } 
    } catch (error) {
      console.log(error);
    }
  }
  
  const handleImageClick = async (id) => {
    try {
      const response = await fetch(`/itemData?id=${encodeURIComponent(id)}`);
      if (response.ok) {
        const result = await response.json();
        setItemData(result);
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


        <div className='box'>
          <div className='productInfo'>
            <AddItemForm onFormSubmit={handleFormSubmit}/>
            <div className='productName'>
              <p>{itemData}</p>
            </div>
          </div>
        </div>
        

        <div className='box'>
          <div className='itemSide'>
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
                  <Item item={item} onImageClick={handleImageClick}/>
                </div>
              ))}
            </div>
          </div>
        </div>


      </div>
    </div>
  );
}

export default App;