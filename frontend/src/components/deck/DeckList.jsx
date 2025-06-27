import List from "../List";
import RemoveCircle from "../../assets/RemoveCircle.svg?react"

const DeckList = ({ decks, handleDeckDelete }) => {
  return (
    <List
      items={decks}
      baseLink="/decks"
      onClickItemIcon={handleDeckDelete}
      itemIcon={RemoveCircle}
    />
  )
};

export default DeckList
