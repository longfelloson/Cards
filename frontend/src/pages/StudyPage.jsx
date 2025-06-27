import { useEffect, useState } from "react";
import { fetchDecks } from "../components/deck/utils";
import { fetchDeckById } from "../components/deck/utils";
import { fetchCardsByDeckId } from "../components/card/utils";
import StudyDeck from "../components/study/StudyDeck";
import Layout from "../components/Layout";
import List from "../components/List";
import NotFound from "../components/NotFound";

const StudyPage = () => {
  const [decksToStudy, setDecksToStudy] = useState([]);
  const [deckToStudy, setDeckToStudy] = useState(null);
  const [deckCards, setDeckCards] = useState([]);
  const [studiedCardsAmount, setStudiedCardsAmount] = useState(0)

  const fetchDecksToStudy = async () => {
    const data = await fetchDecks({ to_study: true });
    setDecksToStudy(data);
  };

  const resetDeckToStudy = () => {
    setDeckToStudy(null)
  };

  const handleDeckSelect = async (deck_id) => {
    const deck = await fetchDeckById({ deck_id: deck_id })
    setDeckToStudy(deck);
    const cards = await fetchCardsByDeckId({ deck_id: deck.id, to_study: true });
    setDeckCards(cards);
    console.log("cards", cards)
  };

  useEffect(() => { 
    fetchDecksToStudy(); 
  }, []);
  
  return (
    <Layout>
      {deckToStudy ? (
        <StudyDeck deck={deckToStudy} cards={deckCards} onReset={resetDeckToStudy} />
      ) : decksToStudy.length ? (
        <>
          <h1 className="font-bold text-2xl">Decks to study:</h1>
          <List 
            items={decksToStudy}
            onClickItem={handleDeckSelect}
          />
        </>
      ) : (
        <NotFound />
      )}
    </Layout>
  );
};

export default StudyPage