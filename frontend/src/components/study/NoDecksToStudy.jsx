import Checkmark from "../../../public/assets/icons/Checkmark.svg?react"

const NoDecksToStudy = ({ text }) => {
  return (
    <div className="place-items-center">
      <Checkmark className="mb-4"/>
      <h1 className="text-2xl">You've studied all decks!</h1>
    </div>
  )
}

export default NoDecksToStudy
