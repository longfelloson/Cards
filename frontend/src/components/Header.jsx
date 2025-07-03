import { useState } from "react";
import { Link } from "react-router-dom";
import { logout } from "../utils";

const HeaderModal = ({ onClose }) => {
  return (
    <>
      <div className="fixed inset-0 z-40" onClick={onClose}></div>
      <div className="modal absolute z-50 bg-blue-500 top-22 right-14 px-6 py-4 rounded">
        <ul className="flex flex-col gap-4 text-white cursor-pointer">
          <li><Link to="/login">Login</Link></li>
          <li onClick={logout}>Logout</li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>
      </div>
    </>
  );
};

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    { label: "Decks", path: "/decks" },
    { label: "Study", path: "/study" },
  ];

  return (
    <header className="grid h-20 w-full grid-cols-12 items-center bg-[#3B82F6] px-6 text-white md:px-14">
      <nav className="col-span-10">
        <ul className="flex h-full cursor-pointer items-center gap-6 text-base font-medium sm:gap-10 md:gap-12 md:text-lg">
          {menuItems.map((item) => (
            <li key={item.path} className="hover:underline">
              <Link to={item.path}>{item.label}</Link>
            </li>
          ))}
        </ul>
      </nav>
      <div className="col-span-2 logo flex justify-end" onClick={() => setIsOpen(prev => !prev)}>
        <svg
          className="h-8 w-8 md:h-10 md:w-10 cursor-pointer"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#ffffff"
        >
          <path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Z" />
        </svg>
      </div>
      { isOpen && <HeaderModal onClose={() => setIsOpen(false)}/> }
    </header>
  );
};

export default Header;
