import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Directory.css';

const Directory = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [file, setFile] = useState(null);
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const profilePictureUrl = 'https://blog-img.speedcurve.com/img/473/tim-circle-blog.png?auto=format,compress&fit=max&w=2000';

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleImageUpload = (e) => {
    setImage(URL.createObjectURL(e.target.files[0]));
  };

  const handleSave = () => {
    const alertBox = document.createElement('div');
    alertBox.style.position = 'fixed';
    alertBox.style.top = '50%';
    alertBox.style.left = '50%';
    alertBox.style.transform = 'translate(-50%, -50%)';
    alertBox.style.backgroundColor = 'white';
    alertBox.style.color = 'black';
    alertBox.style.padding = '50px'; 
    alertBox.style.borderRadius = '10px';
    alertBox.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.3)'; 
    alertBox.style.textAlign = 'center';
    alertBox.style.zIndex = '1000';
    alertBox.style.fontSize = '20px';
  
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '10px';
    closeButton.style.right = '10px';
    closeButton.style.background = 'transparent';
    closeButton.style.border = 'none';
    closeButton.style.fontSize = '24px';
    closeButton.style.cursor = 'pointer';
    closeButton.onclick = () => {
      alertBox.remove();
      overlay.remove();
    };
  
    alertBox.innerHTML = `
      <strong style="font-size: 26px;">Patient Saved!</strong><br/><br/>
      <div style="text-align: center;">
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <button id="surgeryPlansBtn" style="
        background-color: #023047;
        color: white;
        padding: 15px 35px;
        border: none;
        border-radius: 15px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 20px;
      ">Surgery Plans</button>
      </div>
    `;
  
    alertBox.appendChild(closeButton);
  
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'; 
    overlay.style.zIndex = '999';
  
    document.body.appendChild(overlay);
    document.body.appendChild(alertBox);

    document.getElementById('surgeryPlansBtn').onclick = () => {
      alertBox.remove();
      overlay.remove();
      navigate('/surgery-plans');
      
    };
  
    setTimeout(() => {
      alertBox.remove();
      overlay.remove();
    }, 5000); 
  };   
  

  return (
    <div className="directory-page">
      <div className="grid-container">
        <div className="patient-photo">
        <img src={profilePictureUrl} alt="Profile" className="uploaded-photo" />
        </div>

        <div className="patient-info">
          <h2>Patient Information</h2>
          <div className="form-container">
            <div className="input-field">
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter patient name"
              />
            </div>

            <div className="input-field">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter patient email"
              />
            </div>

            <div className="input-field">
              <label htmlFor="file">Upload File:</label>
              <input
                type="file"
                id="file"
                onChange={handleFileUpload}
                className="upload-file-btn"
              />
            </div>

            <div className="input-field">
              <label htmlFor="file">Upload Images:</label>
              <input
                type="file"
                id="file"
                onChange={handleFileUpload}
                className="upload-file-btn"
              />
            </div>

            <button className="save-btn" onClick={handleSave}>
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Directory;
