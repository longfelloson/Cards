import { useState } from "react";
import { EditOutlined, CheckOutlined } from "@ant-design/icons";
import axios from "axios";

const Card = ({ card }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [newFace, setNewFace] = useState("");
    const [newTurnover, setNewTurnover] = useState("");

    const startEditing = () => {
        setNewFace(card.face);
        setNewTurnover(card.turnover);
        setIsEditing(true);
    };

    const updateCard = async () => {
        try {
            await axios.patch(`/api/cards/${card.id}`, {
                face: newFace,
                turnover: newTurnover,
            });
            card.face = newFace
            card.turnover = newTurnover
            setIsEditing(false);
        } catch (error) {
            console.error("Error updating card:", error);
        }
    };

    return (
        <div className="deck-card relative flex flex-col justify-center w-[300px] p-8 m-2 border gap-4 border-black rounded shadow">
            {isEditing ? (
                <>
                    <input
                        value={newFace}
                        onChange={(e) => setNewFace(e.target.value)}
                        className="border p-1 rounded"
                        placeholder="New face"
                        autoFocus
                    />
                    <input
                        value={newTurnover}
                        onChange={(e) => setNewTurnover(e.target.value)}
                        className="border p-1 rounded"
                        placeholder="New turnover"
                    />
                </>
            ) : (
                <>
                    <p className="font-semibold">{card.face}</p>
                    <p className="text-gray-600">{card.turnover}</p>
                </>
            )}

            <div
                className="absolute top-2 right-2 text-gray-500 hover:text-black cursor-pointer"
                onClick={isEditing ? updateCard : startEditing}
            >
                {isEditing ? <CheckOutlined /> : <EditOutlined />}
            </div>
        </div>
    );
};

export default Card;
