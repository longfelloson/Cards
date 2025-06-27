import RemoveCircle from "../../assets/RemoveCircle.svg?react"
import Edit from "../../assets/Edit.svg?react"
import { useState } from "react";
import { updateCardById, deleteCardById } from "../card/utils"
import CardUpdate from "./CardUpdate";

const CardItem = ({ card, handleCardUpdate, handleCardDelete }) => {
  const [isEditing, setIsEditing] = useState(false)

  const updateCard = async ({ newFace, newTurnover }) => {
    const updatedCard = await updateCardById({
      card_id: card.id,
      face: newFace,
      turnover: newTurnover,
    })
    setIsEditing(false)
    handleCardUpdate({ updatedCard })
  }

  const deleteCard = async () => {
    await deleteCardById({ card_id: card.id })
    handleCardDelete({ deletedCardId: card.id })
  };

  return (
    isEditing ? (
      <CardUpdate card={card} updateCard={updateCard}/>
    ) : (
        <div className="flex justify-between rounded-md bg-blue-300 p-4 transition-colors duration-300 ease-in-out hover:bg-blue-400">
          <div className="flex flex-col">
            <span className="mb-2">{card.face}</span>
            <span>{card.turnover}</span>
          </div>
          <div className="flex flex-col justify-start h-full gap-2 items-start">
            <Edit onClick={() => {setIsEditing(true)}}/>
            <RemoveCircle onClick={() => {deleteCard({ card_id: card.id })}}/>
          </div>
        </div>
      )
    )
};

export default CardItem;
