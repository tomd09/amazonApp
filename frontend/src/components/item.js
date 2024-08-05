import React from 'react';

export function Item(props) {

    const { item } = props; 

    return (
        <div className='itemCard'>
            <div className='container'>
                <div className='box itemImageBox'>
                    <img src={`${process.env.PUBLIC_URL}/images/${item['Image Link']}`} alt={item.Name} className='itemImage'/>
                </div>
                <div className='box itemInfo'>
                    <h2>{item.Name}</h2>
                    <p>{item.Type}</p>
                    <p>{item.Price === 'Not Available' ? 'Not Available' : `$${item.Price}`}</p> 
                    <p>As of {item.Time}</p>
                </div>
            </div>
        </div>
    )
}