import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './assets/styles.css';

import Home from './pages/Home';
import UserPage from './pages/UserPage';
import ProductPage from './pages/ProductPage';
import Navbar from './components/Navbar';
import { StrategyProvider } from './context/StrategyContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <StrategyProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/user/:id" element={<UserPage />} />
          <Route path="/product/:id" element={<ProductPage />} />
        </Routes>
      </StrategyProvider>
    </BrowserRouter>
  </React.StrictMode>
);
