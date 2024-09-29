import React, { useState, useEffect } from 'react';
import { Subheading, Navbar } from '../../components';
import fade from '../../images/fade.png';
import './Header.css';

const Header = () => {
  return (
  <div className="full">
    <div className="app-header" id="home" >
      <img src={fade} alt="fade" className="fade-image" />
      <div className='app__wrapper_info'>
        <Subheading/>
      </div>
      <div className="image-title-overlay">
        <h1 className='title-big'>surgARy</h1>
        <h2 className="title-text">Transforming surgical outcomes through cutting-edge assistive technology.
        </h2>
      </div>
    </div>
    <div className='slider'>
      <span>Recent News:</span>
    </div>
    <div className='scroll'>
      <div className="scroll-images">
        <img src="/path/to/image1.jpg" alt="one" />
        <img src="/path/to/image2.jpg" alt="two" />
        <img src="/path/to/image3.jpg" alt="three" />
      </div>
    </div>
  </div>
);
};

export default Header;
