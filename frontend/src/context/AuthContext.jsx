import React, { createContext, useState, useEffect, useContext } from 'react';
import apiService from './apiService';

// Create context
const AuthContext = createContext(null);

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Check for existing user session on component mount
  useEffect(() => {
    const token = sessionStorage.getItem('token');
    const savedUser = sessionStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error("Failed to parse saved user:", error);
        logout();
      }
    } else {
      logout(); // Auto logout if no token or user
    }
    
    setLoading(false);
  }, []);
  const login = async (userOrCredentials) => {
    try {  
        // If the input is a user object (has id), just set it directly
        if (userOrCredentials.id) {
            sessionStorage.setItem('token', userOrCredentials.token); // Store in sessionStorage
            sessionStorage.setItem('user', JSON.stringify(userOrCredentials));
            setUser(userOrCredentials);
            return { user: userOrCredentials };
        }

        // Otherwise, treat it as credentials
        const credentials = userOrCredentials;

        // ✅ Ensure both fields exist before sending request
        if (!credentials.email || !credentials.password) {
            throw new Error("Email and password are required");
        }

        const response = await apiService.login(credentials);
        if (!response.token) {
            throw new Error('Login failed: No token received');
        }

        // Store data in sessionStorage
        sessionStorage.setItem('token', response.token);
        sessionStorage.setItem('user', JSON.stringify(response.user));
        setUser(response.user);

        return response;
    } catch (error) {
        console.error("Login failed:", error);
        throw new Error(error.message || "Login failed");
    }
};

const register = async (userData) => {
    try {
        const response = await apiService.register(userData);
        if (!response.token) {
            throw new Error('Registration failed: No token received');
        }

        // Store data in sessionStorage instead of localStorage
        sessionStorage.setItem('token', response.token);
        sessionStorage.setItem('user', JSON.stringify(response.user));
        setUser(response.user);

        return response;
    } catch (error) {
        console.error("Registration failed:", error);
        throw new Error(error.message || "Registration failed");
    }
  };

  
  // Logout function
  const logout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    setUser(null);
  };
  
  // Update user data
  const updateUserData = (userData) => {
    setUser(userData);
    sessionStorage.setItem('user', JSON.stringify(userData));
  };
  
  // Context value
  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUserData,
    isAuthenticated: !!user
  };
  
  return (
    <AuthContext.Provider value={value}>
      { !loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook for using auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;