import CollectionSearch from "./CollectionSearch";
import CollectionList from "./CollectionList";
import { useEffect, useState } from "react";
import api from "../../api";
import Layout from "../MainLayout";

const CollectionPage = () => {
    const [collections, setCollections] = useState([]);

    const fetchCollections = () => {
        const params = {
            offset: 0,
            limit: 10
        }
        api.get("/collections", { params }).then(response => {setCollections(response.data)})
    };

    useEffect(
        () => {fetchCollections()}, []
    )

    return (
        <Layout>
            <CollectionSearch/>
            <CollectionList collections={collections}/>
        </Layout>
    )
};

export default CollectionPage
