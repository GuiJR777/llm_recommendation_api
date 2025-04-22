import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { StrategyContext } from '../context/StrategyContext';
import './Navbar.css';

function Navbar() {
  const {
    recommendationStrategy,
    setRecommendationStrategy,
    llmStrategy,
    setLLMStrategy
  } = useContext(StrategyContext);

  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="navbar-home" onClick={() => navigate('/')}>
          <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 0 24 24" width="22" fill="white">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
        </span>
        <span className="navbar-title">LLM Recommender Test</span>
      </div>

      <div className="navbar-dropdowns">
        <label>
          Recomendação:
          <select
            value={recommendationStrategy}
            onChange={(e) => setRecommendationStrategy(e.target.value)}
          >
            <option value="history">Histórico</option>
            <option value="preference">Preferência</option>
          </select>
        </label>

        <label>
          Descrição:
          <select
            value={llmStrategy}
            onChange={(e) => setLLMStrategy(e.target.value)}
          >
            <option value="emulator">Emulador</option>
            <option value="chatgpt">ChatGPT</option>
          </select>
        </label>
      </div>
    </nav>
  );
}

export default Navbar;
