import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import { deleteDeck, fetchDeckById } from "../components/deck/utils";
import Deck from "../components/deck/Deck";
import CardList from "../components/card/CardList";
import { fetchCardsByDeckId, updateCardById } from "../components/card/utils";
import Search from "../components/Search";
import CardCreate from "../components/card/CardCreate";

const DeckPage = () => {
  const { deck_id } = useParams();
  const [deck, setDeck] = useState(null);
  const [cards, setCards] = useState([]);

  useEffect(() => {
    const fetchDeck = async () => {
      try {
        const deckData = await fetchDeckById({ deck_id });
        setDeck(deckData);
      } catch (error) {
        console.error("Ошибка при загрузке колоды:", error);
      }
    };

    fetchDeck();
  }, [deck_id]);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const cardsData = await fetchCardsByDeckId({ deck_id, to_study: false });
        console.log("cards data:", cardsData)
        setCards(cardsData);
      } catch (error) {
        console.log("Failed to fetch cards:", error)
      }
    };

    fetchCards();
  }, [deck_id])

  const onSearch = async (query) => {
    const params = { deck_id, to_study: false };

    if (query && query.trim() !== "") {
      params["query"] = query;
    }

    const data = await fetchCardsByDeckId(params);
    setCards(data);
  };

  const handleCardUpdate = ({ updatedCard }) => {
    setCards(prevCards => 
      prevCards.map(card => 
        card.id === updatedCard.id ? updatedCard : card 
      )
    )
  };

  const handleDeckDelete = async () => {
    await deleteDeck({ deck_id: deck.id })
    window.location.href = "/decks"
  };

  const handleCardDelete = ({ deletedCardId }) => {
    setCards(prevCards => prevCards.filter(card => card.id !== deletedCardId))
  };

  const handleCardCreate = ({ createdCard }) => {
    setCards(prevCards => [createdCard, ...prevCards])
  };

  return (
    <Layout>
      {deck ? <Deck deck={deck} onClickDeleteIcon={handleDeckDelete} /> : <p>Загрузка колоды...</p>}
      <CardCreate deck_id={deck_id} handleCardCreate={handleCardCreate} />
      <Search placeholder={"Search a card by its name"} onSearch={onSearch}/>
      <CardList cards={cards} handleCardDelete={handleCardDelete} handleCardUpdate={handleCardUpdate}/>
    </Layout>
  );
};

export default DeckPage;
