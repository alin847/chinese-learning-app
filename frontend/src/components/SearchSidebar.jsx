import "../pages/Search.css";

function SearchSidebar({ items, active_item, onItemClick }) {

    return (
        <div className="search-sidebar">
            {items && items.length > 0 ? (
                    items.map((item, idx) => (
                        <SearchSidebarItem 
                            key={idx} 
                            item={item} 
                            active={active_item.simplified_id === item.simplified_id}
                            onClick={onItemClick}
                        />
                    ))
                ) : (
                    <h2 className="search-sidebar-header">No results, try a new search</h2>
                ) 
            }
        </div>
    );
}

function SearchSidebarItem({ item , active, onClick}) {

    return (
        <div
            className={`search-sidebar-item${active ? ' active' : ''}`}
            onClick={() => onClick(item)}
        >
            <h2 className="search-sidebar-item-l1">
                <strong>{item.simplified}</strong> ({item.pinyin})
            </h2>
            <p className="search-sidebar-item-l2">
                {item.definitions.map((def, i) => (
                    <span key={i}>
                        <strong>{i + 1}.</strong> {def}{'  '}
                    </span>
                ))}
            </p>
        </div>
    )
};

export default SearchSidebar;