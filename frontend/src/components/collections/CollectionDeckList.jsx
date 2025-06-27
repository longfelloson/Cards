import CollectionDeck from "./CollectionDeck";

const CollectionDeckList = ({ decks }) => {
    return (
        <div className="collection-decks grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            {decks.map(deck => (<CollectionDeck key={deck.id} deck={deck}/>))}
        </div>
    )
};

export default CollectionDeckList