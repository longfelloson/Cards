import Item from "./Item";

const List = ({ 
  items,
  baseLink = null,
  onClickItemIcon = null,
  itemIcon = null,
  onClickItem = null,
}) => {
  return (
    <div className="itemList w-full grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4">
      {items.map(item => (
        <Item 
          key={item.id} 
          item={item}
          icon={itemIcon}
          onClickIcon={() => {onClickItemIcon(item.id)}}
          baseLink={baseLink}
          onClickItem={onClickItem}
        />
      ))}
    </div>
  )
};

export default List
