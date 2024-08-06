import React, { useState, useEffect } from 'react';
import './App.css'
import AddItemForm from './components/addItemForm';
import { Item } from './components/item';
import LineChart from './components/lineChart';

function App(){
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('All');
  const [amazonItems, setAmazonItems] = useState([]);
  const [fetchDataTrigger, setFetchDataTrigger] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);
  const [itemData, setItemData] = useState({ time: [], price: [], title: '' });

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

  //fetches all data initially but also filters on select. Initial load will grab first item to fill itemData
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/data?option=${encodeURIComponent(selectedOption)}`);
        if (response.ok) {
          const result = await response.json();
          setAmazonItems(result);
          if (initialLoad) {
            fetchItemData(result[0].Link)
            setInitialLoad(false);
          }
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
  }, [selectedOption, fetchDataTrigger, initialLoad]);

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
        await response.json().then(() => {});
        setFetchDataTrigger(true);
      } 
    } catch (error) {
      console.log(error);
    }
  }

  const fetchItemData = async (id) => {
    try {
      const response = await fetch(`/itemData?id=${encodeURIComponent(id)}`);
      if (response.ok) {
        const result = await response.json();
        const parsedData = JSON.parse(result);
        const time = parsedData.data.map(row => row[2]);
        const price = parsedData.data.map(row => row[1]);
        const title = parsedData.data[0][0];
        setItemData({ time, price, title});
      }
    } catch (error) {
      console.log(error);
    }
  }

  const handleImageClick = (id) => {
    fetchItemData(id);
  }

  function containsOnlyNulls(arr) {
    return arr.every(item => item === null);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Amazon Web Scraper</h1>
      </header>
      <div className='container'>


        <div className='box'>
          <div className='productInfo'>
            <div className='newProductForm'>
              <AddItemForm onFormSubmit={handleFormSubmit}/>
            </div>
            <div className='productPlot'>
              {containsOnlyNulls(itemData.price) ? (
                <p>There is no pricing data for this product</p>
              ) : (
                <LineChart time={itemData.time} price={itemData.price} title={itemData.title}/>
              )}
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