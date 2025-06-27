import CollectionItem from "./CollectionItem";

const CollectionList = ({ collections }) => {
    return (
        <section>
            {collections.map(collection => (
                <CollectionItem key={collection.id} collection={collection} />
            ))}
        </section>
    )
};

export default CollectionList;
