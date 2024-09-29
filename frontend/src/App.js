import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import SignUp from './components/SignUp/SignUp';
import LogIn from './components/LogIn/LogIn';
import Header from './container/Header/Header';
import Directory from './container/Directory/Directory';
import AboutUs from './container/AboutUs/AboutUs';
import { Navbar } from './components';
import './App.css';
import Footer from './components/Footer/Footer';
import SurgeryPlans from './components/SurgeryPlans/SurgeryPlans'

const App = () => (
  <Router> 
    <Navbar/>
      <Routes>
        <Route path="/" element={<Header/>}/>
        <Route path="/portal" element={<Directory/>}/>
        <Route path="/surgery-plans" element={<SurgeryPlans />} />
        <Route path="/about" element={<AboutUs/>}/>
        <Route path="/signup" element={<SignUp/>} /> 
        <Route path="/login" element={<LogIn/>} /> 
      </Routes>
      <Footer/>
  </Router>
);

export default App;
