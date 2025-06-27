const StudyDeckFinished = ({ studiedCardsAmount, onReset }) => {
    return (
        <div className="flex flex-col gap-4 bg-gray-300 p-10 place-items-center">
            <h1 className="lg:text-2xl">You've studied all cards from the deck 🎉</h1>
            <span className="lg:text-xl">Cards studied: {studiedCardsAmount}</span>
            <button 
                className="bg-blue-500 text-white py-4 px-8 rounded"
                onClick={onReset}
            >
                Study
            </button>
        </div>
    )
};

export default StudyDeckFinished
