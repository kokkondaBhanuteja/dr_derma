// Home.jsx
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h2>Your Personalized Skincare Journey</h2>
          <p>Get expert recommendations tailored to your unique skin needs.</p>

          {/* Show "Start Your Routine" only for logged-in users */}
          {isAuthenticated ? (
            <Link to="/questionnaire" className="btn primary-btn">Start Your Routine</Link>
          ) : (
            <div className="button-group">
              <Link to="/register" className="btn primary-btn">Get Started</Link>
              <Link to="/login" className="btn secondary-btn">Login</Link>
            </div>
          )}
        </div>
        <div className="hero-image">
          <img src="/images/skincare-hero.jpg" alt="Skincare products arranged on a clean surface" />
        </div>
      </section>

      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-clipboard-list"></i>
          </div>
          <h3>Personalized Assessment</h3>
          <p>Answer a few questions about your skin and concerns.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-camera"></i>
          </div>
          <h3>Skin Analysis</h3>
          <p>Upload a photo for AI-powered skin analysis.</p>

          {/* Hide "Upload Photo" until user logs in */}
          {isAuthenticated ? (
            <Link to="/photo-upload" className="btn secondary-btn">Upload Photo</Link>
          ) : (
            <Link to="/login" className="btn secondary-btn">Login to Upload</Link>
          )}
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-flask"></i>
          </div>
          <h3>Product Recommendations</h3>
          <p>Receive curated product suggestions based on your needs.</p>
        </div>
      </section>

      <section className="testimonials">
        <h2>Success Stories</h2>
        <div className="testimonial-container">
          <div className="testimonial">
            <p>"Dr. Derma completely transformed my skincare routine. The personalized recommendations actually worked for my sensitive skin!"</p>
            <div className="testimonial-author">— Sarah T.</div>
          </div>

          <div className="testimonial">
            <p>"I've struggled with acne for years. After following Dr. Derma's routine for just 3 weeks, I noticed significant improvement."</p>
            <div className="testimonial-author">— Michael L.</div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
