import React from 'react';
import signin from '../../images/signin.jpg';
import './SignUp.css';

const SignUp = () => {
  return (
    <div className='signup-pg'>
      <div className='grid-container'>
        <div className='section'>
          <h1>Sign Up</h1>
          <div className='form-container p__opensans'>

            <div className='input-field'>
              <label htmlFor='email'>Email</label>
              <input type='email' id='email' placeholder='Enter your email' />
            </div>
            
            <div className='input-field'>
              <label htmlFor='password'>Password</label>
              <input type='password' id='password' placeholder='Enter your password' />
            </div>

            <button className='sign-in-btn'>Sign Up</button>

          </div>

          <div className='log-in'>
            Already have an account? <a href='/login'>Log In</a>
          </div>
        </div>
        <div className='sign-image'>
            <img src={signin} alt="signin" className="si-image" />
        </div>
      </div>
    </div>
  );
};

export default SignUp;
