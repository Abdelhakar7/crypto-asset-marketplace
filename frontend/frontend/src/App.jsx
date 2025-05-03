import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Navbar from './Components/Navbar/Navbar'
import MainPage from './pages/main_page'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/explore" element={<div className="page-container"><h1>Explore Assets</h1></div>} />
        <Route path="/assets" element={<div className="page-container"><h1>All Assets</h1></div>} />
        <Route path="/create" element={<div className="page-container"><h1>Create Asset</h1></div>} />
        <Route path="/profile" element={<div className="page-container"><h1>Profile</h1></div>} />
        <Route path="/login" element={<div className="page-container"><h1>Sign In</h1></div>} />
        <Route path="/signup" element={<div className="page-container"><h1>Sign Up</h1></div>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
