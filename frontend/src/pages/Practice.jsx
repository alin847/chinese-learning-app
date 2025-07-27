import HeaderHome from "../components/HeaderHome";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import HomeSidebar from "../components/HomeSidebar";
import { fetchAPI_JSON } from "../utils/api";
import { useEffect } from "react";

function Practice() {
  // Check if user is new
  const [newUser, setNewUser] = useState(false);
  useEffect(() => {
    async function checkUserProgress() {
      const data = await fetchAPI_JSON('/api/progress/', { method: 'GET' });
      if (data.learning_count + data.reviewing_count + data.mastered_count === 0) {
        setNewUser(true);
      }
    }
    checkUserProgress();
  }, []);


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
                <img src="/mixed.png" />
                <h3>mixed practice</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/dictation-sentence')}>
                <img src="/sentdict.png" />
                <h3>sentence dictation</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/dictation-simplified')}>
                <img src="/chardict.png" />
                <h3>character dictation</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/writing')}>
                <img src="/writing.png" />
                <h3>sentence writing</h3>
              </div>
              <div className="card" onClick={() => handleCardClick('/practice/speaking')}>
                <img src="/speaking.png" />
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
