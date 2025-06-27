import { updateCardById } from "../card/utils";

const StudyDeckCardsButtons = ({ card, onClick }) => {
  const buttons = [
    { label: "Again", color: "bg-red-500", hover: "hover:bg-red-400", value: "again" },
    { label: "Hard", color: "bg-orange-500", hover: "hover:bg-orange-400", value: "hard" },
    { label: "Good", color: "bg-green-500", hover: "hover:bg-green-400", value: "good" },
    { label: "Easy", color: "bg-cyan-500", hover: "hover:bg-cyan-400", value: "easy" },
  ];

  const onClickButton = async (event) => {
    const last_memorization_level = event.target.value;

    try {
      await updateCardById({ card_id: card.id, last_memorization_level });
      if (onClick) {
        onClick();
      }
    } catch (error) {
      console.error("Failed to update card:", error);
    }
  };

  return (
    <div className="buttons grid grid-cols-2 md:grid-cols-4 gap-2">
      {buttons.map(({ label, color, value, hover }) => (
        <button
          key={label}
          value={value}
          className={`text-white ${color} ${hover} rounded p-2 md:p-4 transition-colors duration-300 ease-in-out`}
          onClick={onClickButton}
        >
          {label}
        </button>
      ))}
    </div>
  );
};

export default StudyDeckCardsButtons;
