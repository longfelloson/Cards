import { useState } from "react";
import CollectionDeckList from "./CollectionDeckList";

const CollectionItem = ({ collection }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(prev => !prev);

  return (
    <div className="collection text-xl">
      <h2 className="flex p-2 bg-gray-200 shadow-md rounded my-4 justify-between items-center">
        <span>{collection.name}</span>
        <svg
          className="h-7 cursor-pointer"
          onClick={toggle}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 -960 960 960"
          fill="#000000"
        >
          <path d={isOpen
            ? "M480-528 296-344l-56-56 240-240 240 240-56 56-184-184Z" // стрелка вниз
            : "M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"} // стрелка вверх
          />
        </svg>
      </h2>

      {isOpen && <CollectionDeckList decks={collection.decks} />}
    </div>
  );
};

export default CollectionItem;
