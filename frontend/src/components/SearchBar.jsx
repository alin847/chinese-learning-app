import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSearch } from "react-icons/fi";
import './SearchBar.css'; // Import your CSS styles

function SearchBar() {
    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [debounceTimer, setDebounceTimer] = useState(null);

    const navigate = useNavigate();
    const inputRef = useRef(null);
    const dropdownRef = useRef(null);

    // Helper Functions
    const cleanQuery = (input) => {
        if (!isEnglishMode) {
            return input.trim().replace(/[0-9\s]/g, '');
        } else {
            return input.trim();
        }
    };
    const getQueryType = (query) => {
        if (isEnglishMode) return 'definitions';

        const hasChinese = /[\u4e00-\u9fff]/.test(query);
        if (hasChinese) return 'simplified';
        return 'pinyin';
    };

    const fetchSearchResults = async (query) => {
        if (!query) {
            setShowDropdown(false);
            return;
        }
        const cleanedQuery = cleanQuery(query);
        const queryType = getQueryType(query);
        const url = `http://localhost:4000/api/search?${queryType}=${encodeURIComponent(cleanedQuery)}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();

            if (data.length === 0) {
                setShowDropdown(false);
                return;
            }

            // Limit to 5 results
            setSearchResults(data.slice(0, 5));
            setShowDropdown(true);
        } catch (error) {
            console.error('Error fetching search results:', error);
            setShowDropdown(false);
        }
    };

    const handleInputChange = (e) => {
        setQuery(e.target.value);

        // Clear previous debounce timer
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }

        // Set new debounce timer
        const timer = setTimeout(() => {
            fetchSearchResults(query);
        }, 100); // 100ms debounce time

        setDebounceTimer(timer);
    };

    // Handle Enter key press
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            const cleanedQuery = cleanQuery(query);
            const type = getQueryType(cleanedQuery);
            if (cleanedQuery) {
                // Navigate to search results page
                setShowDropdown(false);
                navigate(`/search/${type}/${encodeURIComponent(cleanedQuery)}`);
            }
        }
    };

    // Handle dropdown item click
    const handleDropdownItemClick = (item) => {
        navigate(`/search/id/${item.simplified_id}`);
        setShowDropdown(false);
        setQuery(''); // Clear input after selection
    };

    // Hide dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(e.target) &&
                e.target !== inputRef.current
            ) {
                setShowDropdown(false);
            }
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, []);

    // Cleanup timer on unmount
    useEffect(() => {
        return () => {
            if (debounceTimer) {
                clearTimeout(debounceTimer);
            }
        };
    }, [debounceTimer]);

    // Search Toggle State
    const [isEnglishMode, setIsEnglishMode] = useState(() => {
        // Check local storage for saved mode
        const savedMode = localStorage.getItem('isEnglishMode');
        return savedMode ? JSON.parse(savedMode) : false; // Default to false if not set
    });

    // Handle toggle change
    const handleToggleChange = (checked) => {
        setIsEnglishMode(checked);
        localStorage.setItem('isEnglishMode', JSON.stringify(checked)); // Save to local storage
    };

    return (
        <div className="search-bar">
            <div className="search-input-wrapper">
                {/* Search icon */}
                <FiSearch className="search-icon" />

                {/* Search input */}
                <input
                    type="text"
                    id="search-input"
                    placeholder="What do you want to learn?"
                    ref={inputRef}
                    value={query}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />

                {/* Search toggle */}
                <SearchToggle isChecked={isEnglishMode} onChange={handleToggleChange} />

                {/* Search dropdown */}
                {showDropdown && (
                    <div className="search-dropdown" id="search-dropdown" ref={dropdownRef}>
                        {searchResults.map((item) => (
                            <SearchDropdownItem
                                key={item.simplified_id}
                                item={item}
                                onClick={() => handleDropdownItemClick(item)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function SearchDropdownItem({ item, onClick }) {
    return (
        <div className="search-dropdown-item" onClick={onClick}>
            <div className="search-dropdown-line1">
                {item.simplified} ({item.pinyin})
            </div>
            <div className="search-dropdown-line2">
                {item.definitions.map((def, i) => `${i + 1}. ${def}`).join('  ')}
            </div>
        </div>
    );
}

function SearchToggle({ isChecked, onChange }) {
    return (
        <div className="lang-toggle">
            <input
                type="checkbox"
                id="lang-switch"
                checked={isChecked}
                onChange={(e) => onChange(e.target.checked)}
            />
            <label htmlFor="lang-switch" id="lang-label"></label>
        </div>
    );
}


export default SearchBar;