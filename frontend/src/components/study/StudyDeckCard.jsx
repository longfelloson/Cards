import { useEffect, useState } from "react";
import StudyDeckCardButtons from "./StudyDeckCardButtons"

const StudyDeckCard = ({ card, onClickButton }) => {
    const [isFlipped, setIsFlipped] = useState(false);

    useEffect(() => {
      setIsFlipped(false)
    }, [card])
    
    return (
      <section className="flex flex-col gap-4">
        <div 
          className={
            `rounded text-center text-white font-2xl 
            p-10 transition-colors duration-300 
            ease-in-out shadow
            ${isFlipped ? 'bg-blue-400' : 'bg-[#3B82F6]' }`
          }
          onClick={() => setIsFlipped(prev => !prev)}
        >
          <span>{isFlipped ? card.turnover : card.face }</span>
        </div>
        { isFlipped && <StudyDeckCardButtons card={card} onClick={onClickButton}/> }
      </section>
    );
}

export default StudyDeckCard;