import React from 'react';
import signin from '../../images/signin.jpg';
import './LogIn.css';

const LogIn = () => {
  return (
    <div className='login-pg'>
      <div className='grid-container'>
        <div className='section'>
          <h1>Login</h1>
          <div className='form-container p__opensans'>

            <div className='input-field'>
              <label htmlFor='email'>Email</label>
              <input type='email' id='email' placeholder='Enter your email' />
            </div>
            
            <div className='input-field'>
              <label htmlFor='password'>Password</label>
              <input type='password' id='password' placeholder='Enter your password' />
            </div>

            <button className='log-in-btn'>Login</button>

          </div>

          <div className='sign-in'>
            Don't have an account yet? <a href='/signup'>Sign Up</a>
          </div>
        </div>
        <div className='login-image'>
            <img src={signin} alt="signin" className="si-image" />
        </div>
      </div>
    </div>
  );
};

export default LogIn;
