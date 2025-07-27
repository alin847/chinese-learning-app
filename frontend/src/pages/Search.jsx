import SearchSidebar from "../components/SearchSidebar";
import HeaderHome from "../components/HeaderHome";
import SearchContent from "../components/SearchContent";
import SearchPlaceholder from "../components/SearchPlaceholder";
import { useState, useEffect } from "react";
import { useLocation, useParams } from "react-router-dom";
import Loading from "../components/Loading";
import "./Search.css";
import { fetchAPI_JSON } from "../utils/api";

function Search() {
    const location = useLocation();
    const params = useParams();

    // Determine which route was matched
    const getRouteType = () => {
        if (location.pathname === '/search/recommended') {
            return 'RECOMMENDED';
        }
        if (params.type && params.query) {
            return 'SEARCH_RESULTS';
        }
        if (location.pathname === '/search') {
            return 'SEARCH_HOME';
        }
        return 'UNKNOWN';
    };
    // Get the route type
    const routeType = getRouteType();

    // State variables
    const [searchResults, setSearchResults] = useState([]);
    const [activeItem, setActiveItem] = useState({});
    const [loading, setLoading] = useState(true);
    const [placeHolder, setPlaceholder] = useState(false);

    useEffect(() => {
        if (routeType === 'SEARCH_HOME') {
            // Handle search home logic
            // This could be fetching recommended items or showing a welcome message
            setPlaceholder(true);
            setLoading(false);
        } else if (routeType === 'RECOMMENDED') {
            // Fetch recommended items
            setLoading(true);
            fetchSearchResults('/api/search/recommended');
            setPlaceholder(false);
        } else if (routeType === 'SEARCH_RESULTS') {
            // Fetch search results based on params.type and params.query
            setLoading(true);
            fetchSearchResults(`/api/search/${params.type}/${params.query}`);
            setPlaceholder(false);
        } else {
            console.error('Unknown route type:', routeType);
            setSearchResults([]);
            setActiveItem({});
        }
    }, [routeType, params]);

    const fetchSearchResults = async (url) => {
        try {
            const data = await fetchAPI_JSON(url, {
                method: 'GET',
            });

            if (data && data.length > 0) {
            setSearchResults(data);
            setActiveItem(data[0]);
            } else {
            setSearchResults([]);
            setActiveItem({});
            }
        } catch (err) {
            console.error('Error fetching search results:', err);
            setSearchResults([]);
            setActiveItem({});
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <Loading />;
    }
    if (placeHolder) {
        return (
            <>
            <HeaderHome />
            <SearchPlaceholder />
            </>
        );
    }

    return (
        <div className="search-page">
                <HeaderHome />
                <div className="search-container">
                    <SearchSidebar 
                        items={searchResults} 
                        active_item={activeItem}
                        onItemClick={(item) => setActiveItem(item)}
                    />
                    <SearchContent 
                        active_item={activeItem} 
                        setActiveItem={setActiveItem}
                        setSearchResults={setSearchResults}
                    />
                </div>
        </div>
    )
}

export default Search;