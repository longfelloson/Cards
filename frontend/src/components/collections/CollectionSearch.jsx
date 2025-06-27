import { useState } from "react";

const CollectionSearch = () => {
    const [collection, setCollection] = useState(null);

    const fetchCollectionByInput = () => {}

    return (
        <section>
            <input 
                onChange={fetchCollectionByInput}
                className="mt-4 w-full rounded-md border-2 border-blue-300 px-4 py-2" 
                placeholder="Type a name of a deck"
            />
        </section>
    )
};

export default CollectionSearch
