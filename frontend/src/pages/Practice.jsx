
import HeaderHome from "../components/HeaderHome";
import { useNavigate } from "react-router-dom";
import HomeSidebar from "../components/HomeSidebar";

function Practice() {
  const navigate = useNavigate();
  return (
    <div className="practice">
      <HeaderHome />
      
      <div className="home-container">
        <HomeSidebar activePage="practice" />

        <main className="content">
          <h1>Practice</h1>
          
          <div className="subcontent">
            <div className="cards">
                <div className="card">
                    <img src="https://placehold.co/150x150" onClick={() => navigate('/practice/mixed')}/>
                    <h3>mixed practice</h3>
                </div>

                <div className="card" onClick={() => navigate('/practice/dictation-sentence')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>sentence dictation</h3>
                </div>

                <div className="card" onClick={() => navigate('/practice/dictation-simplified')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>character dictation</h3>
                </div>

                <div className="card" onClick={() => navigate('/practice/writing')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>sentence writing</h3>
                </div>
                
                <div className="card" onClick={() => navigate('/practice/speaking')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>speaking</h3>
                </div>
            </div>
          </div>


        </main>

      </div>
    </div>
  )
};

export default Practice;