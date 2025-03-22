// App.jsx - Main React Component with Auth Integration
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';

// Importing my components
import Home from './components/Home';
import Questionnaire from './components/Questionnaire';
import Recommendations from './components/Recommendations';
import Profile from './components/Profile';
import PhotoUpload from './components/PhotoUpload';
import Login from './components/Login';
import Register from './components/Register';

// Import auth context
import { AuthProvider, useAuth } from './context/AuthContext';

// ProtectedRoute component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Redirect non-authenticated users when they click links on Home


// Navigation component
const Navigation = () => {
  const { isAuthenticated, logout, user } = useAuth();
  
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        {isAuthenticated ? (
          <>
            <li><Link to="/questionnaire">Questionnaire</Link></li>
            <li><Link to="/recommendations">Recommendations</Link></li>
            <li><Link to="/profile">Profile</Link></li>
            <li><Link to="/photo-upload">Photo Analysis</Link></li>
            <li>
              <button onClick={logout} className="logout-btn">
                Logout ({user?.username || "User"})
              </button>
            </li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

// App wrapper with auth provider
const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

// Main app content
const AppContent = () => {
  const [skinData, setSkinData] = useState(null);

  return (
    <div className="app">
      <header>
        <div className="logo">
          <h1>Dr. Derma</h1>
        </div>
        <Navigation />
      </header>

      <main>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginRedirect />} />
          <Route path="/register" element={<RegisterRedirect />} />

          {/* Protected routes */}
          <Route path="/questionnaire" element={<ProtectedRoute><Questionnaire setSkinData={setSkinData} /></ProtectedRoute>} />
          <Route path="/recommendations" element={<ProtectedRoute><Recommendations skinData={skinData} /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/photo-upload" element={<ProtectedRoute><PhotoUpload setSkinData={setSkinData} /></ProtectedRoute>} />

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <footer>
        <p>© 2025 Dr. Derma. All rights reserved.</p>
      </footer>
    </div>
  );
};


// Login & Register Redirect Components
const LoginRedirect = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div>Loading...</div>;  
  return isAuthenticated ? <Navigate to="/" replace /> : <Login />;
};

const RegisterRedirect = () => {
  const { isAuthenticated, loading } = useAuth();
  if(loading) return <div> Loading...</div>
  return isAuthenticated ? <Navigate to="/" replace /> : <Register />;
};




export default App;
