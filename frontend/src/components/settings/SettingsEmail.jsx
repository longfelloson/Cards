import { useState } from "react";
import Edit from "../../assets/Edit.svg?react";
import Close from "../../assets/Close.svg?react";
import Check from "../../assets/Check.svg?react";
import { sendVerificationEmail } from "./utils";

const SettingsEmail = ({ user }) => {
  const [newEmail, setNewEmail] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isConfirmed, setIsConfirmed] = useState(false);

  const handleCancel = () => {
    setNewEmail('');
    setIsEditing(false);
  };

  const handleConfirm = () => {
    try {
      sendVerificationEmail(user.id, newEmail)
    } catch (error) {
      console.log("Failed to send verification email:", error)
    } finally {
      setIsConfirmed(true);
      setIsEditing(false);
      alert("Verification link has been sent to your new email")
    }
  };

  return (
    <div className="flex justify-between items-center col-span-2 row-span-3 rounded-md p-4 bg-gray-200 gap-4">
      {!isEditing ? (
        <>
          <span className="lg:w-[80%] lg:text-3xl">{user.email}</span>
          <Edit
            className="h-full rounded-md bg-blue-500 p-2 cursor-pointer"
            fill="white"
            onClick={() => setIsEditing(true)}
          />
        </>
      ) : (
        <>
          <input
            className="w-[80%] text-3xl px-2 py-1 rounded-md border border-gray-400"
            type="email"
            placeholder="Enter new email"
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
            required
          />
          <div className="flex flex-col justify-between w-12 gap-2 h-full">
            <Close
              className="w-full h-1/2 rounded-md bg-blue-500 p-2 cursor-pointer"
              fill="white"
              onClick={handleCancel}
            />
            <Check
              className="w-full h-1/2 rounded-md bg-blue-500 p-2 cursor-pointer"
              fill="white"
              onClick={handleConfirm}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default SettingsEmail;
