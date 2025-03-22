import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function PhotoUpload({ setSkinData }) {
  const navigate = useNavigate();
  const [photo, setPhoto] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPhoto(file);
      const fileReader = new FileReader();
      fileReader.onload = () => {
        setPreviewUrl(fileReader.result);
      };
      fileReader.readAsDataURL(file);
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!photo) return;
    
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('image', photo);
    
    try {
      const response = await fetch(`/api/analysis/upload`, {
        method: 'POST',
        body: formData,
        // Add authentication header
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload image');
      }
      
      const data = await response.json();
      setSkinData(data);
      navigate('/recommendations');
    } catch (error) {
      console.error('Error uploading photo:', error);
      setError('Failed to upload image. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="photo-upload">
      <h2>Upload Your Skin Photo</h2>
      <p>Take a clear, well-lit photo of your face to receive AI-powered skin analysis</p>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="upload-area">
          {previewUrl ? (
            <div className="preview">
              <img src={previewUrl} alt="Skin preview" />
              <button 
                type="button" 
                className="btn secondary-btn"
                onClick={() => {
                  setPhoto(null);
                  setPreviewUrl(null);
                }}
              >
                Remove
              </button>
            </div>
          ) : (
            <div className="dropzone" 
                 onClick={() => document.getElementById('file-input').click()}
                 style={{
                   border: '2px dashed #ccc',
                   borderRadius: '8px',
                   padding: '40px 20px',
                   textAlign: 'center',
                   cursor: 'pointer',
                   backgroundColor: '#f9f9f9'
                 }}>
              <i className="fas fa-camera" style={{ fontSize: '48px', color: '#666', marginBottom: '15px' }}></i>
              <p>Drag & drop your photo here or click to select</p>
              <input 
                id="file-input"
                type="file" 
                accept="image/*" 
                onChange={handleFileChange}
                required
                style={{ display: 'none' }}
              />
            </div>
          )}
        </div>
        
        <div className="photo-tips">
          <h3>Tips for best results:</h3>
          <ul>
            <li>Use natural lighting</li>
            <li>Take photo without makeup</li>
            <li>Capture your entire face</li>
            <li>Avoid heavy filters or editing</li>
          </ul>
        </div>
        
        <button 
          type="submit" 
          className="btn primary-btn"
          disabled={!photo || loading}
          style={{
            marginTop: '20px',
            width: '100%'
          }}
        >
          {loading ? "Analyzing..." : "Analyze My Skin"}
        </button>
      </form>
    </div>
  );
}

export default PhotoUpload;