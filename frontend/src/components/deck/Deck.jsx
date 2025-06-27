import { useEffect, useState } from "react";
import CardList from "../card/CardList";
import { fetchCardsByDeckId } from "../card/utils";
import RemoveCircle from '../../assets/RemoveCircle.svg?react';

const Deck = ({ deck, onClickDeleteIcon }) => {
  return (
    <div className="deck w-full">
      <div className="text-white flex flex-col gap-2 shadow-md rounded-md bg-blue-500 p-4 transition-colors duration-300 ease-in-out hover:bg-blue-400">
        <span className="flex flex-row justify-between text-lg font-semibold">
          { deck.name }
            <RemoveCircle onClick={onClickDeleteIcon} />
          </span>
          <span className="text-sm">{ deck.name }</span>
          <span className="text-sm">{ deck.name }</span>
        </div>
    </div>
  );
};

export default Deck;
