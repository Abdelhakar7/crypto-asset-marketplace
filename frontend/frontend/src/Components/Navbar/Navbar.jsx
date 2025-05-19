import React, { useState } from 'react';
import './Navbar.css';
import LoginModal from '../Login/Login';

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [loginModalOpen, setLoginModalOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const openLoginModal = () => {
    setLoginModalOpen(true);
  };

  const closeLoginModal = () => {
    setLoginModalOpen(false);
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-logo">
            <a href="/">
              <span className="logo-text">Crypto</span>
              <span className="logo-accent">Market</span>
            </a>
          </div>

          <div className="navbar-search">
            <input type="text" placeholder="Search assets..." />
            <button className="search-button">
              <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </div>

          <button className={`menu-toggle ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
            <span></span>
            <span></span>
            <span></span>
          </button>

          <div className={`navbar-links ${menuOpen ? 'active' : ''}`}>
            <ul>
              <li><a href="/explore">Explore</a></li>
              <li><a href="/assets">Assets</a></li>
              <li><a href="/create">Create</a></li>
              <li className="dropdown">
                <a href="/profile">Profile</a>
                <div className="dropdown-content">
                  <a href="/profile/settings">Settings</a>
                  <a href="/profile/assets">My Assets</a>
                  <a href="/profile/favorites">Favorites</a>
                </div>
              </li>
            </ul>
            <div className="navbar-buttons">
              <button onClick={openLoginModal} className="sign-in-btn">Login</button>
              <a href="/connect" className="connect-wallet-btn">Connect Wallet</a>
            </div>
          </div>
        </div>
      </nav>

      <LoginModal 
        isOpen={loginModalOpen} 
        onClose={closeLoginModal} 
      />
    </>
  );
};

export default Navbar;
