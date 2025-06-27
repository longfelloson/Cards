import StudyDeckCard from "./StudyDeckCard";
import StudyDeckFinished from "./StudyDeckFinished";
import { useState } from "react";

const StudyDeck = ({ deck, cards, onReset }) => {
  const [studiedCardsAmount, setStudiedCardsAmount] = useState(0);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);

  const onClickButton = () => {
    setStudiedCardsAmount(prev => prev + 1);
    setCurrentCardIndex(prev => prev + 1);
  };

  const hasFinished = currentCardIndex >= cards.length;

  if (cards.length === 0) {
    return <p>No cards for studying</p>
  }

  if (hasFinished) {
    return <StudyDeckFinished onReset={onReset} studiedCardsAmount={studiedCardsAmount} />
  }

  return (
      <div className="w-full flex flex-col gap-4">
        <h1 className="">{deck.name}</h1>
        <StudyDeckCard card={cards[currentCardIndex]} onClickButton={onClickButton} />
      </div>
    )
};

export default StudyDeck;
