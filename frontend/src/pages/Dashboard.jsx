import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import HeaderHome from '../components/HeaderHome'
import HomeSidebar from '../components/HomeSidebar'
import Loading from '../components/Loading'

function Dashboard() {
  const [user, setUser] = useState(null)
  const [newUser, setNewUser] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token) {
      navigate('/')
      return
    }
    
    if (userData) {
      // Fetch user vocab data to see if user is new
      fetch('http://localhost:4000/api/progress/', {
        method: 'GET',
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.learning_count + data.reviewing_count + data.mastered_count === 0) {
          setNewUser(true)
        } else {
          setNewUser(false)
        }
        setUser(JSON.parse(userData))
      })
      .catch(err => {
        console.error('Error fetching vocab data:', err)
        setNewUser(false)
      })
    }
  }, [navigate])

  const handleCardClick = (path) => {
    if (newUser) {
      alert("You must add vocabulary words before starting.");
    } else {
      navigate(path);
    }
  };
  if (!user) {
    return <Loading />
  }

  return (
    <div className="dashboard">
      <HeaderHome />
      
      <div className="home-container">
        <HomeSidebar activePage="dashboard" />

        <main className="content">
          <h1>Welcome back, {user.name}!</h1>
          
          {newUser && (
          <div className="subcontent">
            <h2>Getting Started</h2>
            <div className="horizontal-line"></div>
            <div className="cards">
                <div className="card" onClick={() => navigate("/placement")}>
                    <img src="https://placehold.co/150x150"/>
                    <h3>take a test to automatically setup</h3>
                </div>
                <div className="card" onClick={() => navigate('/search')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>add words to learn manually</h3>
                </div>
            </div>
          </div>
          )}

          <div className="subcontent">
            <h2>Recommended</h2>
            <div className="horizontal-line"></div>
            <div className="cards">
                <div className="card" onClick={() => handleCardClick("/practice/mixed")} >
                    <img src="https://placehold.co/150x150"/>
                    <h3>mixed practice</h3>
                </div>
                <div className="card" onClick={() => navigate('/search/recommended')}>
                    <img src="https://placehold.co/150x150" />
                    <h3>discover new words</h3>
                </div>
            </div>
          </div>
        </main>

      </div>
    </div>
  )
}

export default Dashboard;
