import React, {useState} from 'react';

function AddItemForm({ onFormSubmit }) {
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
        await onFormSubmit(itemData);
        setItemUrl('');
        setItemName('');
        setItemType('');
            
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