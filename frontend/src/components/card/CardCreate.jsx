import { useState } from "react";
import { createCard } from "./utils";
import CheckCircle from "../../assets/CheckCircle.svg?react"

const CardCreate = ({ deck_id, handleCardCreate }) => {
  const [face, setFace] = useState('')
  const [turnover, setTurnover] = useState('')

  const onClickCreateCard = async () => {
    const createdCard = await createCard({ face, turnover, deck_id })
    setFace('')
    setTurnover('')
    handleCardCreate({ createdCard })
  };

  return (
    <div className="cardCreate w-full flex justify-between">
      <input
        className="w-4/10 border-2 border-blue-500 p-2 bg-gray-200 rounded"
        value={face}
        onChange={(e) => {setFace(e.target.value)}}
        placeholder="Enter the face to create a card"
      />
      <input
        className="w-4/10 border-2 border-blue-500 p-2 bg-gray-200 rounded"
        value={turnover}
        onChange={(e) => {setTurnover(e.target.value)}}
        placeholder="Enter the turnover to create a card"
      />
      <CheckCircle onClick={() => {onClickCreateCard()}}/>
    </div>
  )
};

export default CardCreate