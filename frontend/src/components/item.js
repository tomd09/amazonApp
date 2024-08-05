import React from 'react';

export function Item(props) {

    const { item } = props; 
    const imageLink = '/amazonApp/backend/images/' + item['Image Link'];
    console.log(imageLink);
    return (
        <div className='itemCard'>
            <div className='container'>
                <div className='box itemImage'>
                    <img src={imageLink} alt={item.Name}/>
                </div>
                <div className='box itemInfo'>
                    <h2>{item.Name}</h2>
                    <p>Type: {item.Type}</p>
                    <p>Price: {item.Price}</p> 
                    <p>As of {item.Time}</p>
                    <p>Image Link: {item['Image Link']}</p>
                </div>
            </div>
        </div>
    )
}