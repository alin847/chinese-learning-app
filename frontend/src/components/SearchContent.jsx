import { GiSpeaker } from "react-icons/gi";
import { IoAddCircle, IoRemoveCircle } from "react-icons/io5";
import { VscSearchStop } from "react-icons/vsc";
import "../pages/Search.css";

function SearchContent({ active_item, setActiveItem, setSearchResults }) {

    return (
        <div className="search-content">
            {active_item && Object.keys(active_item).length > 0 ? (
                <>
                    <SearchContentHeader 
                        active_item={active_item} 
                        setActiveItem={setActiveItem}
                        setSearchResults={setSearchResults}
                    />
                    <SearchContentDefinitions active_item={active_item} />
                    <SearchContentExamples active_item={active_item} />
                </>
            ) : (
                <div className="search-content-center">
                    <VscSearchStop size={"50%"} color="#ddd" />
                </div>
            )}
        </div>
    )
}


function SearchContentHeader({ active_item, setActiveItem, setSearchResults }) {
    return (
        <div className="search-content-header">
            <h1>
                <span>{active_item.simplified} ({active_item.pinyin})</span>
                <span
                    className="audio-icon"
                    onClick={() => playAudio({ text: active_item.simplified })}
                >
                    <GiSpeaker size={44} color="black"/>
                </span>
            </h1>

            {active_item.is_added ? (
                <IoRemoveCircle
                    className="add-vocab-icon"
                    size={44}
                    onClick={() => addRemoveVocab({ item: active_item, setSearchResults, setActiveItem })}
                />
            ) : (
                <IoAddCircle
                    className="add-vocab-icon"
                    size={44}
                    onClick={() => addRemoveVocab({ item: active_item, setSearchResults, setActiveItem })}
                />
            )    
            }
        </div>
    )
};

function SearchContentDefinitions({ active_item }) {
   
    return (
        <div className="search-content-definitions">
            <h2>Definitions</h2>
            <div className="horizontal-line"></div>
            <ol>
                {active_item.definitions.map((def, idx) => (
                    <li key={idx}>{def}</li>
                ))}
            </ol>
        </div>
    )
};

function SearchContentExamples({ active_item }) {
    return (
        <div className="search-content-examples">
            <h2>Sentence Examples</h2>
            <div className="horizontal-line"></div>
            {active_item.sentences.length > 0 ? (
                active_item.sentences.map((sentence, idx) => (
                    <div key={idx} className="sentence-example">
                        <div className="sentence-chinese">
                            <span><strong>{sentence.chinese}</strong> ({sentence.pinyin})</span>
                            <span className="audio-icon" onClick={() => playAudio({ text: sentence.chinese})}>
                                <GiSpeaker size={24} color="black"/>
                            </span>
                        </div>

                        <div className="sentence-translation">{sentence.english}</div>
                    </div>
                ))
            ) : (
                <p>No examples available.</p>
            )}
        </div>
    )
};

function addRemoveVocab({ item, setSearchResults, setActiveItem }) {
    const is_added = item.is_added
    const userStr = localStorage.getItem('user');
    const user = userStr ? JSON.parse(userStr) : null;
    const url = `http://localhost:4000/api/vocab`;

    if (is_added) {
        // Remove from vocabulary
        const confirmRemove = confirm(`Are you sure you want to remove "${item.simplified}" from your vocabulary? Removing it will delete all your learning progress with this word.`);
        if (!confirmRemove) return;

        fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ simplified_id: item.simplified_id })
        })
        .then(response => {
            if (response.ok) {
                setSearchResults(prev => 
                    prev.map(i => i.simplified_id === item.simplified_id ? { ...i, is_added: false } : i)
                );
                setActiveItem(prev => ({
                    ...prev,
                    is_added: false
                })
                );
            } else {
                console.error('Failed to remove vocabulary:', response.statusText)
            }
        })
        .catch(err => {
            console.error('Error removing vocabulary:', err)
        })
    } else {
        // Add to vocabulary
        fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ simplified_id: item.simplified_id })
        })
        .then(response => {
            if (response.ok) {
                    setSearchResults(prev => 
                        prev.map(i => i.simplified_id === item.simplified_id ? { ...i, is_added: true } : i)
                    );
                    setActiveItem(prev => ({
                        ...prev,
                        is_added: true
                    }));
            } else {
                console.error('Failed to add vocabulary:', response.statusText)
            }
        })
        .catch(err => {
            console.error('Error adding vocabulary:', err)
        })
    }
};


const audioCache = new Map();

function playAudio({ text }) {
    if (audioCache.has(text)) {
        const cachedUrl = audioCache.get(text);
        const audio = new Audio(cachedUrl);
        audio.play();
        return;
    }

    fetch('http://localhost:4000/api/tts', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    })
    .then(response => response.blob())
    .then(blob => {
        const audioUrl = URL.createObjectURL(blob);
        audioCache.set(text, audioUrl);
        const audio = new Audio(audioUrl);
        audio.play();
    })
    .catch(err => {
        console.error('Error fetching audio:', err);
    });
}

export default SearchContent;