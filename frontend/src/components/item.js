import React from 'react';

export function Item({item, onImageClick}) {
    return (
        <div className='itemCard'>
            <div className='container'>
                <div className='box itemImageBox'>
                    <img src={`images/${item['Image Link']}`} 
                         alt={item.Name} 
                         className='itemImage' 
                         onClick={() => onImageClick(item.Link)}/>
                </div>
                <div className='box itemInfo'>
                    <h2>{item.Name}</h2>
                    <p>{item.Type}</p>
                    <p>{item.Price === 'Not Available' ? 'Unavailable' : `$${item.Price}`}</p> 
                    <p>As of {item.Time}</p>
                </div>
            </div>
        </div>
    );
}