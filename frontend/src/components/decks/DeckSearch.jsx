import { useState } from "react";

const DeckSearch = () => {
  const [name, setName] = useState('');

  return (
    <form
      className="flex border border-gray-200 rounded-md p-4 shadow-sm bg-white"
    >
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter the name to find a deck"
        className="border border-gray-200 w-full rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </form>
  );
}

export default DeckSearch
