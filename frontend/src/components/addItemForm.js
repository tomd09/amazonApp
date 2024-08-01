import React, {useState} from 'react';

function AddItemForm() {
    const [itemUrl, setItemUrl] = useState('');
    const [itemName, setItemName] = useState('');
    const [itemType, setItemType] = useState('');

    const handleUrlChange = (e) => setItemUrl(e.target.value);
    const handleNameChange = (e) => setItemName(e.target.value);
    const handleTypeChange = (e) => setItemType(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const itemData = {
            itemUrl,
            itemName,
            itemType
        }
        try {
            const response = await fetch('/addItem', {
                method: 'POST',
                body: JSON.stringify(itemData),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                alert('Item added successfully');
                setItemUrl('');
                setItemName('');
                setItemType('');
            } else {
                const errorData = await response.json();
                alert(`Failed to add item: ${errorData.error}`);
            }
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type='text' value={itemUrl} onChange={handleUrlChange} placeholder='Enter Amazon Product URL' required />
            <br />
            <input type='text' value={itemName} onChange={handleNameChange} placeholder='Enter Product Name' required />
            <br/>
            <input type='text' value={itemType} onChange={handleTypeChange} placeholder='Enter Product Type' required />
            <br/>
            <button type='submit'>Add Item</button>
        </form>
    );
}

export default AddItemForm;