import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiService from '../context/apiService';

function Questionnaire({ setSkinData }) {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    skinType: "",
    concerns: [],
    diet: "",
    hydration: "",
    sleep: "",
    lifestyle: "",
    location: "",
    allergies: "",
    dietPreferences: []
  });

  const handleSelection = (field, value) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  const handleMultiSelection = (field, value, e) => {
    if (e) e.preventDefault();
    setFormData((prevState) => {
      const updatedValues = prevState[field].includes(value)
        ? prevState[field].filter((item) => item !== value)
        : [...prevState[field], value];
      return { ...prevState, [field]: updatedValues };
    });
  };

  const handleTextInput = (field, e) => {
    setFormData({
      ...formData,
      [field]: e.target.value,
    });
  };

  const nextStep = () => setCurrentStep(currentStep + 1);
  const prevStep = () => setCurrentStep(currentStep - 1);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    if (currentStep !== 4) {
        console.log('Form submitted from incorrect step:', currentStep);
        return;
    }  // Now we have 4 steps
    
    try {
      console.log('the form Data is = ', formData);
      const skinData = {
        skinType: formData.skinType || "Unknown",
        concerns: Array.isArray(formData.concerns) ? formData.concerns : [],
        diet: formData.diet || "Unknown",
        hydration: formData.hydration || "Unknown",
        sleep: formData.sleep || "Unknown",
        lifestyle: formData.lifestyle || "Unknown",
        location: formData.location || "Unknown",
        allergies: formData.allergies || "None",
        dietPreferences: Array.isArray(formData.dietPreferences) ? formData.dietPreferences : []
      };
      
      // Use the apiService to send data to backend
      const analysisData = await apiService.analyzeSkinFromQuestionnaire(skinData);

      setSkinData({
        skinType: formData.skinType,
        concerns: formData.concerns,
        location: formData.location,
        allergies: formData.allergies,
        dietPreferences: formData.dietPreferences,
        ...analysisData.analysis.recommendations
      });
      
      navigate('/recommendations');
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <div className="questionnaire">
      <h2>Let's Create Your Personalized Skincare & Diet Plan</h2>
      <p>
        Answer a few questions so we can tailor the best routine for you based on your skin needs and local diet options.
      </p>

      <div className="progress-bar">
        <div
          className="progress"
          style={{ width: `${(currentStep / 4) * 100}%` }}
        ></div>
      </div>

      <form onSubmit={handleSubmit}>
        {currentStep === 1 && (
          <div className="form-step">
            <h3>How does your skin feel on most days?</h3>
            <div className="option-group">
              {["Dry", "Oily", "Combination", "Normal", "Sensitive"].map(
                (type) => (
                  <button
                    type="button"
                    key={type}
                    className={formData.skinType === type ? "selected" : ""}
                    onClick={() => handleSelection("skinType", type)}
                  >
                    {type}
                  </button>
                )
              )}
            </div>

            <h3>What are your biggest skin concerns?</h3>
            <div className="option-group">
              {[
                "Acne",
                "Wrinkles",
                "Hyperpigmentation",
                "Redness",
                "Dryness",
                "Dark Circles",
                "Large Pores",
                "Uneven Texture"
              ].map((concern) => (
                <button
                  type="button"
                  key={concern}
                  className={
                    formData.concerns.includes(concern) ? "selected" : ""
                  }
                  onClick={(e) => handleMultiSelection("concerns", concern, e)}
                >
                  {concern}
                </button>
              ))}
            </div>

            <h3>Do you have any allergies or sensitivities?</h3>
            <div className="form-group">
              <textarea
                placeholder="E.g., Fragrance, Nuts, Dairy, etc."
                value={formData.allergies}
                onChange={(e) => handleTextInput("allergies", e)}
              ></textarea>
            </div>

            <button
              type="button"
              className="btn primary-btn"
              onClick={nextStep}
            >
              Next
            </button>
          </div>
        )}

        {currentStep === 2 && (
          <div className="form-step">
            <h3>How's your diet?</h3>
            <div className="option-group">
              {[
                "Balanced",
                "High in processed foods",
                "Vegetarian",
                "Vegan",
                "Low in fruits/vegetables",
                "High in sugar",
                "Low in protein"
              ].map((diet) => (
                <button
                  type="button"
                  key={diet}
                  className={formData.diet === diet ? "selected" : ""}
                  onClick={() => handleSelection("diet", diet)}
                >
                  {diet}
                </button>
              ))}
            </div>

            <h3>What are your dietary preferences?</h3>
            <div className="option-group">
              {[
                "Local/Traditional foods",
                "Mediterranean",
                "Low-carb",
                "Plant-based",
                "Gluten-free",
                "Dairy-free",
                "Keto",
                "Paleo"
              ].map((preference) => (
                <button
                  type="button"
                  key={preference}
                  className={
                    formData.dietPreferences.includes(preference) ? "selected" : ""
                  }
                  onClick={(e) => handleMultiSelection("dietPreferences", preference, e)}
                >
                  {preference}
                </button>
              ))}
            </div>

            <h3>How much water do you drink daily?</h3>
            <div className="option-group">
              {["Less than 1L", "1-2L", "More than 2L"].map((hydration) => (
                <button
                  type="button"
                  key={hydration}
                  className={formData.hydration === hydration ? "selected" : ""}
                  onClick={() => handleSelection("hydration", hydration)}
                >
                  {hydration}
                </button>
              ))}
            </div>

            <button
              type="button"
              className="btn secondary-btn"
              onClick={prevStep}
            >
              Back
            </button>
            <button
              type="button"
              className="btn primary-btn"
              onClick={nextStep}
            >
              Next
            </button>
          </div>
        )}

        {currentStep === 3 && (
          <div className="form-step">
            <h3>How's your sleep quality?</h3>
            <div className="option-group">
              {["Poor", "Average", "Good"].map((sleep) => (
                <button
                  type="button"
                  key={sleep}
                  className={formData.sleep === sleep ? "selected" : ""}
                  onClick={() => handleSelection("sleep", sleep)}
                >
                  {sleep}
                </button>
              ))}
            </div>

            <h3>How active is your lifestyle?</h3>
            <div className="option-group">
              {["Sedentary", "Moderately Active", "Very Active"].map(
                (lifestyle) => (
                  <button
                    type="button"
                    key={lifestyle}
                    className={
                      formData.lifestyle === lifestyle ? "selected" : ""
                    }
                    onClick={() => handleSelection("lifestyle", lifestyle)}
                  >
                    {lifestyle}
                  </button>
                )
              )}
            </div>

            <button
              type="button"
              className="btn secondary-btn"
              onClick={prevStep}
            >
              Back
            </button>
            <button
              type="button"
              className="btn primary-btn"
              onClick={nextStep}
            >
              Next
            </button>
          </div>
        )}

        {currentStep === 4 && (
          <div className="form-step">
            <h3>Where are you located?</h3>
            <div className="form-group">
              <input
                type="text"
                placeholder="Country or Region"
                value={formData.location}
                onChange={(e) => handleTextInput("location", e)}
              />
              <p className="form-hint">This helps us suggest local food options that are good for your skin</p>
            </div>

            <button
              type="button"
              className="btn secondary-btn"
              onClick={prevStep}
            >
              Back
            </button>
            <button type="submit" className="btn primary-btn">
              Get My Plans
            </button>
          </div>
        )}
      </form>
    </div>
  );
}

export default Questionnaire;