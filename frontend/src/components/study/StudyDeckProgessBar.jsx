const StudyDeckProgressBar = ({ deckCardsAmount, studiedCardsAmount }) => {
  const percentage = Math.round((studiedCardsAmount / deckCardsAmount) * 100);

  return (
    <div className="flex items-center justify-between p-2 rounded border">
      <div className="flex-grow bg-gray-200 rounded-full h-4 overflow-hidden mr-2">
        <div
        className="bg-green-500 h-full transition-all duration-300"
        style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-sm  whitespace-nowrap">
      {studiedCardsAmount} / {deckCardsAmount}
      </span>
    </div>
  );
};

export default StudyDeckProgressBar;

