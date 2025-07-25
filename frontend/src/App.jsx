import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

// Import pages
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Search from './pages/Search'
import Test from './pages/Test'
import Practice from './pages/Practice'
import Vocabulary from './pages/Vocabulary'
import Placement from './pages/Placement'
import Progress from './pages/Progress'
import PrivateRoute from './components/PrivateRoute'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected routes (we'll add authentication later) */}
          <Route path="/home" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/search" element={<PrivateRoute><Search /></PrivateRoute>} />
          <Route path="/search/:type/:query" element={<PrivateRoute><Search /></PrivateRoute>} />
          <Route path="/search/recommended" element={<PrivateRoute><Search /></PrivateRoute>} />
          <Route path="/practice/:type" element={<PrivateRoute><Test /></PrivateRoute>} />
          <Route path="/practice" element={<PrivateRoute><Practice /></PrivateRoute>} />
          <Route path="/vocabulary" element={<PrivateRoute><Vocabulary /></PrivateRoute>} />
          <Route path="/placement" element={<PrivateRoute><Placement /></PrivateRoute>} />
          <Route path="/progress" element={<PrivateRoute><Progress /></PrivateRoute>} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
