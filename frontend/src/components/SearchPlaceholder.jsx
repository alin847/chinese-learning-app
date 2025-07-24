import { TbCloudSearch } from "react-icons/tb";
import "../pages/Search.css";

function SearchPlaceholder() {
    return (
        <div className="search-container">
            <div className="search-sidebar">
                <h2 className="search-sidebar-header">Enter your search above!</h2>
            </div>
            <div className="search-content">
                <div className="search-content-center">
                    <TbCloudSearch size={"50%"} color="#ddd" />
                </div>
            </div>
        </div>
    );
}


export default SearchPlaceholder;