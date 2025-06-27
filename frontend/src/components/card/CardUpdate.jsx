import CheckCircle from "../../assets/CheckCircle.svg?react"
import { useState } from "react";

const CardUpdate = ({ card, updateCard }) => {
  const [newFace, setNewFace] = useState(card.face);
  const [newTurnover, setNewTurnover] = useState(card.turnover);

  return (
      <div className="flex justify-between rounded-md bg-blue-300 p-4 transition-colors duration-300 ease-in-out hover:bg-blue-400">
        <div className="flex flex-col">
          <input
            className="mb-2"
            value={newFace}
            onChange={(e) => {setNewFace(e.target.value)}}
            placeholder="Enter a new face for the card: "
          />
          <input
            value={newTurnover}
            onChange={(e) => {setNewTurnover(e.target.value)}}
            placeholder="Enter a new turnover for the card: "
          />
        </div>
        <div className="flex flex-col justify-start h-full gap-2 items-start">
          <CheckCircle onClick={() => updateCard({ card_id: card.id, newFace, newTurnover })} />
        </div>
      </div>
    );
  };

export default CardUpdate;
