import { useState, useEffect } from "react";
import { useDebouncedValue } from "../utils";


const Search = ({ onSearch, placeholder, style }) => {
  const [query, setQuery] = useState('');
  const debouncedValue = useDebouncedValue(query, 500);

  useEffect(() => {
    if (debouncedValue) {
      console.log("SEARCH:", query)
      onSearch(query);
    }
  }, [debouncedValue]);
  
  return (
    <input
      className="shadow-md rounded-md p-4 bg-gray-200 w-full"
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder={placeholder}
    />
  )
};

export default Search