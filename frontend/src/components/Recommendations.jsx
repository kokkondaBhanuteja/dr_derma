import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import html2pdf from "html2pdf.js";

function Recommendations({ skinData }) {
  const [routine, setRoutine] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!skinData) return;
    setLoading(true);
    setTimeout(() => {
      setRoutine(skinData); // Use AI-generated routine from props
      setLoading(false);
    }, 1500); // Simulated loading delay
  }, [skinData]);
  // Function to generate and download PDF
  const generatePDF = () => {
    const element = document.getElementById("recommendations-content");
    const filename = `${skinData.skinType || "Custom"}_Skincare_Plan.pdf`;

    const options = {
      margin: 10,
      filename: filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
    };

    html2pdf().set(options).from(element).save();
  };
  if (loading) {
    return (
      <div className="recommendations loading">
        <div className="loading-spinner"></div>
        <p>Creating your personalized skincare and diet plans...</p>
      </div>
    );
  }

  if (!skinData || !routine) {
    return (
      <div className="recommendations empty-state">
        <h2>No Personalized Plans Yet</h2>
        <p>
          Complete the questionnaire to receive personalized skincare and diet
          recommendations
        </p>
        <div className="button-group">
          <Link to="/questionnaire" className="btn primary-btn">
            Take Questionnaire
          </Link>
        </div>
      </div>
    );
  }

  // Ensure we have the morning and evening routines
  const morningRoutine = skinData.morning_routine || [];
  const eveningRoutine = skinData.evening_routine || [];
  const dietRecommendations = skinData.diet_recommendations || [];

  return (
    <div className="recommendations">
      <div id="recommendations-content" className="recommendations-content">
        <div id="" className="recommendations-header">
          <h2>Your Personalized Skincare & Diet Plans</h2>
          <p>
            Based on your skin type:{" "}
            <span className="highlight">
              {skinData.skinType || "Combination"}
            </span>
          </p>
          <p>
            Addressing concerns:{" "}
            <span className="highlight">
              {skinData.concerns?.join(", ") || "Acne, Hyperpigmentation"}
            </span>
          </p>
          {skinData.location && (
            <p>
              Customized for your location:{" "}
              <span className="highlight">{skinData.location}</span>
            </p>
          )}
        </div>

        <h3 className="section-title">Skincare Routine</h3>
        <div className="routine-container">
          <div className="routine-card morning">
            <div className="routine-header">
              <i className="fas fa-sun"></i>
              <h3>Morning Routine</h3>
            </div>

            <div className="routine-steps">
              {morningRoutine.map((item, index) => (
                <div className="routine-step" key={`morning-${index}`}>
                  <div className="step-number">{index + 1}</div>
                  <div className="step-content">
                    <h4>{item.product_type}</h4>
                    <p>{item.purpose}</p>
                    {item.ingredients_to_look_for && (
                      <div className="ingredients">
                        <small>
                          Key ingredients:{" "}
                          {item.ingredients_to_look_for.join(", ")}
                        </small>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="routine-card evening">
            <div className="routine-header">
              <i className="fas fa-moon"></i>
              <h3>Evening Routine</h3>
            </div>

            <div className="routine-steps">
              {eveningRoutine.map((item, index) => (
                <div className="routine-step" key={`evening-${index}`}>
                  <div className="step-number">{index + 1}</div>
                  <div className="step-content">
                    <h4>{item.product_type}</h4>
                    <p>{item.purpose}</p>
                    {item.ingredients_to_look_for && (
                      <div className="ingredients">
                        <small>
                          Key ingredients:{" "}
                          {item.ingredients_to_look_for.join(", ")}
                        </small>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <h3 className="section-title">Diet Recommendations</h3>
        <div className="diet-container">
          <div className="routine-card diet">
            <div className="routine-header">
              <i className="fas fa-apple-alt"></i>
              <h3>Food for Healthy Skin</h3>
              {skinData.location && (
                <span className="location-tag">
                  Customized for {skinData.location}
                </span>
              )}
            </div>

            <div className="diet-content">
              {dietRecommendations.length > 0 ? (
                <div className="diet-categories">
                  {dietRecommendations.map((category, index) => (
                    <div className="diet-category" key={`diet-${index}`}>
                      <h4>{category.category}</h4>
                      <p>{category.description}</p>
                      <div className="food-items">
                        {category.foods.map((food, foodIndex) => (
                          <div className="food-item" key={`food-${foodIndex}`}>
                            <span className="food-name">{food.name}</span>
                            <span className="food-benefit">{food.benefit}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="diet-placeholder">
                  <p>
                    Based on your skin type ({skinData.skinType}), concerns (
                    {skinData.concerns?.join(", ")}), and location (
                    {skinData.location || "Unknown"}), we recommend foods rich
                    in antioxidants, omega-3 fatty acids, and vitamins A, C, and
                    E. Focus on local fruits, vegetables, and lean proteins.
                  </p>
                  <p>Complete local food recommendations will appear here.</p>
                </div>
              )}

              <div className="diet-tips">
                <h4>General Dietary Tips for Skin Health</h4>
                <ul>
                  <li>Stay hydrated with at least 2L of water daily</li>
                  <li>Reduce processed sugar and refined carbohydrates</li>
                  <li>Include foods rich in zinc and selenium</li>
                  <li>Consume healthy fats like avocados and olive oil</li>
                  <li>Add probiotic foods for gut health</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="recommendations-footer">
        <button onClick={generatePDF} className="btn primary-btn">
          Save Plans
        </button>
        <button className="btn secondary-btn">Share Plans</button>
        <Link to="/questionnaire" className="btn secondary-btn">
          Retake Questionnaire
        </Link>
      </div>
    </div>
  );
}

export default Recommendations;
