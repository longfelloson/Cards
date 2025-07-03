import Mail from "../../assets/Mail.svg?react"
import Password from "../../assets/Password.svg?react"
import Contrast from "../../assets/Contrast.svg?react"

const SettingsList = () => {
  return (
    <div className="settingsList col-span-1 row-span-3 rounded-md p-4 bg-gray-200">
      <ul className="h-full flex flex-col justify-between gap-2">
        <li className="">
          <a href="#email" className="flex gap-2 items-center">
            <Mail />Email
          </a>
        </li>
      </ul>
    </div>
  )
}

export default SettingsList