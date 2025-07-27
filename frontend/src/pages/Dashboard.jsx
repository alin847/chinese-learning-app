import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import HeaderHome from '../components/HeaderHome'
import HomeSidebar from '../components/HomeSidebar'
import Loading from '../components/Loading'
import { fetchAPI_JSON } from '../utils/api'

function Dashboard() {
  const user = JSON.parse(localStorage.getItem('user'))
  const [loading, setLoading] = useState(true)
  const [newUser, setNewUser] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {  
    const fetchData = async () => {
      const data = await fetchAPI_JSON('/api/progress/', { method: 'GET' })
      if (data.learning_count + data.reviewing_count + data.mastered_count === 0) {
        setNewUser(true)
      } else {
        setNewUser(false)
      }
      setLoading(false)
    }
    fetchData()
  }, [navigate])

  const handleCardClick = (path) => {
    if (newUser) {
      alert("You must add vocabulary words before starting.")
    } else {
      navigate(path)
    }
  }

  if (loading) {
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
                  <img src="/testbubble.png" />
                  <h3>take a test to automatically setup</h3>
                </div>
                <div className="card" onClick={() => navigate('/search')}>
                  <img src="/add.png" />
                  <h3>add words to learn manually</h3>
                </div>
              </div>
            </div>
          )}
          <div className="subcontent">
            <h2>Recommended</h2>
            <div className="horizontal-line"></div>
            <div className="cards">
              <div className="card" onClick={() => handleCardClick("/practice/mixed")}>
                <img src="/mixed.png" />
                <h3>mixed practice</h3>
              </div>
              <div className="card" onClick={() => navigate('/search/recommended')}>
                <img src="/lightbulb.png" />
                <h3>discover new words</h3>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
