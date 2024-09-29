import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SurgeryPlans.css';

const SurgeryPlans = () => {
  const [plans, setPlans] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const navigate = useNavigate();
  const profilePictureUrl = 'https://blog-img.speedcurve.com/img/473/tim-circle-blog.png?auto=format,compress&fit=max&w=2000';

  const handleSave = () => {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'; 
    overlay.style.zIndex = '999';
    
    setIsSaved(true);


    setTimeout(() => {
      overlay.remove();
      navigate('/surgery-plans');
    }, 5000);
  };

  return (
    <div className="directory-page"> {}
      <div className="grid-container">
        <div className="patient-photo">
          <img src={profilePictureUrl} alt="Profile" className="uploaded-photo" />
        </div>

        <div className="patient-info">
          <h2>Surgery Plans</h2>
          <div className="form-container">
            <div className="input-field">
              <label htmlFor="plans">Surgery Plans:</label>
              <textarea
                id="plans"
                value={plans}
                onChange={(e) => setPlans(e.target.value)}
                placeholder="Enter surgery plans"
                rows="6"
                style={{ width: '100%' }}
              />
            </div>
            <button
              className="save-btn"
              onClick={handleSave}
              style={{
                backgroundColor: isSaved ? '#ffb703' : '#023047', 
                color: 'white' 
              }}
            >
              {isSaved ? 'Saved' : 'Save'} {}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SurgeryPlans;
