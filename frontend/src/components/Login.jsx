import React, { useState } from 'react';
import {useAuth} from "../context/AuthContext";
import { useNavigate, Link } from 'react-router-dom';
import { useEffect } from 'react';

function Login() { const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);
  //to handle the input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value.trim() // Trim spaces to avoid empty input issues
    }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    //  explicit validation before sending request
    if (!formData.email || !formData.password) {
      setError("Email and password are required");
      return;
  }
    setLoading(true);
    
    try {
      await login(formData);
      // Redirect to home page
      navigate('/');
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login to Dr. Derma</h2>
        <p>Welcome back! Please login to continue your skincare journey.</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="Your email address"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              placeholder="Your password"
            />
          </div>
          
          <button 
            type="submit" 
            className="btn primary-btn" 
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="auth-footer">
          <p>Don't have an account? <Link to="/register">Register</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Login;