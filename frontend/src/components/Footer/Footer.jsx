import React from 'react';
import './Footer.css';

const Footer = () => (
  <footer className="footer">
    <div className="footer-content">
      <p>&copy; {new Date().getFullYear()} surgARy All Rights Reserved.</p>
      <ul className="footer-links">
        <li><a href="/about">About Us</a></li>
        <li><a href="/contact">Contact</a></li>
        <li>Privacy Policy</li>
        <li>Terms of Service</li>
      </ul>
    </div>
  </footer>
);

export default Footer;
