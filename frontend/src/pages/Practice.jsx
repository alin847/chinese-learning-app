import HeaderHome from "../components/HeaderHome";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import HomeSidebar from "../components/HomeSidebar";

function Practice() {
  // Check if user is new
  const [newUser, setNewUser] = useState(false);
  fetch('http://localhost:4000/api/progress/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.learning_count + data.reviewing_count + data.mastered_count === 0) {
        setNewUser(true);
      }
    })
    .catch(err => {
      console.error('Error fetching vocab data:', err);
    });

  const navigate = useNavigate();
  const handleCardClick = (path) => {
    if (newUser) {
      alert("You must add vocabulary words before starting.");
    } else {
      navigate(path);
    }
  };

  return (
    <div className="practice">
      <HeaderHome />
      <div className="home-container">
        <HomeSidebar activePage="practice" />
        <main className="content">
          <h1>Practice</h1>
          <div className="subcontent">
            <div className="cards">
              <div className="card" onClick={() => handleCardClick('/practice/mixed')}>
                <img src="https://placehold.co/150x150" />
                <h3>mixed practice</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/dictation-sentence')}>
                <img src="https://placehold.co/150x150" />
                <h3>sentence dictation</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/dictation-simplified')}>
                <img src="https://placehold.co/150x150" />
                <h3>character dictation</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/writing')}>
                <img src="https://placehold.co/150x150" />
                <h3>sentence writing</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/speaking')}>
                <img src="https://placehold.co/150x150" />
                <h3>speaking</h3>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Practice;
