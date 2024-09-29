import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import logo from '../../images/logo.png';

const Navbar = () => (
  <nav className='nav-bar'>
    <div className='nav-logo'>
      <img src={logo} alt="logo" className="logo-image" />
      <p className='p__opensans' style={{ fontWeight: 'bold', fontSize: '1.5em' }}><Link to="/"> surgARy </Link></p>
    </div>
    <ul className='navbar-links'>
      <li className='p__opensans'>
        <Link to="/"> Home </Link>
      </li>
      <li className='p__opensans'>
        <Link to="/portal"> Check Patients </Link>
      </li>
      <li className='p__opensans'>
        <Link to="/about"> About </Link>
      </li>
    </ul>
    <div className='app__navbar-login'>
      <Link to='/signup' className='p__opensans'>Sign Up</Link>
      <div/>
      <Link to='/login' className='p__opensans'>Login</Link>
    </div>
  </nav>
);

export default Navbar;
