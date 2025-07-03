import Close from "../../assets/Close.svg?react"

const VerificationFailure = () => {
  return (
    <div className="p-4 h-3/8">
      <div className="flex h-full justify-between">
        <h2 className="flex bg-gray-200 rounded-md shadow-md w-5/6 text-3xl justify-center items-center">
          We couldn't verify this link...
        </h2>
        <Close fill="red" className="h-full bg-gray-200 rounded-md shadow-md" />
      </div>
    </div>
  )
};

export default VerificationFailure