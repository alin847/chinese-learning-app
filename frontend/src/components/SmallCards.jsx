import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./SmallCards.css";

function SmallCards({ items }) {
    const [visibleCount, setVisibleCount] = useState(20);

    const loadMore = () => {
        setVisibleCount(prevCount => prevCount + 20);
    };

    return (
        <div className="small-cards">
            {items.slice(0, visibleCount).map((item, index) => (
                <SmallCard
                    key={index}
                    simplified={item.simplified}
                    simplified_id={item.simplified_id}
                />
            ))}
            {visibleCount < items.length && (
                <button className="load-more" onClick={loadMore}>
                    Load More
                </button>
            )}
        </div>
    )
}

function SmallCard( {simplified, simplified_id} ) {
    const navigate = useNavigate();
    const onClick = () => {
        navigate(`/search/id/${simplified_id}`);
    };

    return (
        <div className="small-card" onClick={onClick}>
            <h3>{simplified}</h3>
        </div>
    );
    
}

export default SmallCards;