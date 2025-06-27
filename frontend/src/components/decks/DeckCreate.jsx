import { useState } from "react";
import { createDeck } from "../deck/utils";

const DeckCreate = ({ onCreate }) => {
  const [name, setName] = useState('');

  const handleChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const newDeck  = await createDeck({ name });
      onCreate(newDeck);
    } catch (error) {
      console.log(error)
      alert(error.response.data.detail)
    }

    setName('');
  };

return (
    <form
      className="flex bg-gray-200 rounded-md p-4 shadow-sm"
      onSubmit={handleSubmit}
    >
      <input
        type="text"
        value={name}
        onChange={handleChange}
        placeholder="Enter the name to create a deck"
        className="w-full border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      <button type="submit">
        <svg 
          className="ml-3"
          xmlns="http://www.w3.org/2000/svg" 
          height="24px" 
          viewBox="0 -960 960 960" 
          width="24px" 
          fill="black">
          <path d="M440-280h80v-160h160v-80H520v-160h-80v160H280v80h160v160Zm40 200q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z" />
        </svg>
      </button>
    </form>
  );

}

export default DeckCreate
