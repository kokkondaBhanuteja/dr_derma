
// Profile.jsx
import React, { useState } from 'react';

function Profile() {
  const [user, setUser] = useState({
    name: 'Jamie Smith',
    email: 'jamie.smith@example.com',
    skinType: 'Combination',
    concerns: ['Acne', 'Hyperpigmentation'],
    savedRoutines: [
      { id: 1, name: 'Summer Routine', date: '2025-02-15' },
      { id: 2, name: 'Winter Routine', date: '2025-01-10' }
    ]
  });
  
  const [activeTab, setActiveTab] = useState('info');
  
  return (
    <div className="profile">
      <div className="profile-header">
        <div className="profile-avatar">
          <img src="/images/avatar-placeholder.jpg" alt="User avatar" />
        </div>
        <div className="profile-title">
          <h2>{user.name}</h2>
          <p>Member since January 2025</p>
        </div>
      </div>
      
      <div className="profile-tabs">
        <button 
          className={`tab-button ${activeTab === 'info' ? 'active' : ''}`}
          onClick={() => setActiveTab('info')}
        >
          Personal Info
        </button>
        <button 
          className={`tab-button ${activeTab === 'routines' ? 'active' : ''}`}
          onClick={() => setActiveTab('routines')}
        >
          Saved Routines
        </button>
        <button 
          className={`tab-button ${activeTab === 'progress' ? 'active' : ''}`}
          onClick={() => setActiveTab('progress')}
        >
          Skin Progress
        </button>
      </div>
      
      <div className="profile-content">
        {activeTab === 'info' && (
          <div className="tab-content info-tab">
            <div className="form-group">
              <label>Full Name</label>
              <input type="text" value={user.name} readOnly />
            </div>
            
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" value={user.email} readOnly />
            </div>
            
            <div className="form-group">
              <label>Skin Type</label>
              <input type="text" value={user.skinType} readOnly />
            </div>
            
            <div className="form-group">
              <label>Skin Concerns</label>
              <div className="concern-tags">
                {user.concerns.map((concern, index) => (
                  <span key={index} className="concern-tag">{concern}</span>
                ))}
              </div>
            </div>
            
            <button className="btn primary-btn" onClick={() => setUser({...user, name: 'New Name'})}>
              Edit Profile
            </button>
          </div>
        )}
        
        {activeTab === 'routines' && (
          <div className="tab-content routines-tab">
            <div className="saved-routines">
              {user.savedRoutines.map((routine) => (
                <div className="routine-item" key={routine.id}>
                  <div className="routine-info">
                    <h4>{routine.name}</h4>
                    <p>Created on {routine.date}</p>
                  </div>
                  <div className="routine-actions">
                    <button className="btn secondary-btn">View</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'progress' && (
          <div className="tab-content progress-tab">
            <div className="progress-empty">
              <i className="fas fa-camera-retro"></i>
              <h3>Track Your Skin Journey</h3>
              <p>Upload weekly photos to see how your skin changes over time</p>
              <button className="btn primary-btn">Upload First Photo</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
