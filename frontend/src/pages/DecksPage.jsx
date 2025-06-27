import { useEffect, useState } from "react"
import { fetchDecks, deleteDeck } from "../components/deck/utils"
import DeckList from "../components/deck/DeckList"
import DeckCreate from "../components/decks/DeckCreate"
import Layout from "../components/Layout"
import Search from "../components/Search"

const DecksPage = () => {
  const [decks, setDecks] = useState([]);

  const fetchDecksToDisplay = async () => {
    const data = await fetchDecks();
    setDecks(data);
  };

  useEffect(() => {
    (async () => {
      await fetchDecksToDisplay();
    })();
  }, []);

  const handleDeckCreate = (newDeck) => {
    setDecks(prevDecks => [newDeck, ...prevDecks])
  };

  const handleDeckDelete = async (deck_id) => {
    await deleteDeck({ deck_id });

    setDecks(prevDecks =>
      prevDecks.filter(deck => deck.id !== deck_id)
    );
  };

  const onSearch = async (query) => {
    try {
      const params = {
        to_study: false,
        ...(query?.trim() && { query: query.trim() }),
      };

      const data = await fetchDecks(params);
      setDecks(data);
    } catch (error) {
      console.error("Error searching decks:", error);
    }
  };

  return (
    <Layout>
      <div className="flex flex-col gap-4 w-full">
        <div className="w-full">
          <DeckCreate onCreate={handleDeckCreate} />
        </div>
        { decks.length > 0 ? 
          (
            <>
              <div className="w-full">
                <Search
                  onSearch={onSearch} 
                  placeholder={"Enter the name of a deck to find it"} 
                />
              </div>
              <DeckList decks={decks} handleDeckDelete={handleDeckDelete} />
            </>
          ) : (
            <p>You don't have any decks</p>
          )
        }
      </div>
    </Layout>
  )
}

export default DecksPage
