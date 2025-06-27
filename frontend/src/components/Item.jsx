import { Link } from 'react-router-dom';
import { createElement } from 'react';

const Item = ({ 
  item,
  icon = null,
  onClickIcon = null,
  onClickItem = null,
  baseLink = null,
}) => {
  const content = (
    <div 
      onClick={() => {onClickItem(item.id)}}
      className="flex flex-row justify-between gap-2 rounded-md bg-blue-300 p-4 transition-colors duration-300 ease-in-out hover:bg-blue-400 cursor-pointer"
    >
      <div>
        <span className="flex text-lg font-semibold">
          {item.name}
        </span>
      </div>
    </div>
  )

  if (baseLink) {
    return <Link to={baseLink + `/${item.id}`}>{content}</Link>
  }

  return content
};

export default Item;
