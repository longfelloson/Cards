import { Link } from "react-router-dom";
import Close from "../../assets/Close.svg?react"
import Check from "../../assets/Check.svg?react"

const VerificationSuccess = () => {
  return (
    <div className="p-4 h-3/8">
      <div className="flex h-full justify-between">
        <h2 className="flex bg-gray-200 rounded-md shadow-md w-5/6 text-3xl justify-center items-center">
          Verification has been successful
        </h2>
        <Check fill="green" className="h-full bg-gray-200 rounded-md shadow-md" />
      </div>
    </div>
  )
};

export default VerificationSuccess