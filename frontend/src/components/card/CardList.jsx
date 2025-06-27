import CardItem from "./CardItem";

const CardList = ({ cards, handleCardDelete, handleCardUpdate }) => {
  return (
    <div className="cardsList w-full grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {cards.map(card => (
        <CardItem 
          key={card.id} 
          card={card} 
          handleCardUpdate={handleCardUpdate}
          handleCardDelete={handleCardDelete}
        />
      ))}
    </div>
  )
};

export default CardList