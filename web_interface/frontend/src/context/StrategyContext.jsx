import React, { createContext, useState } from 'react';

export const StrategyContext = createContext();

export const StrategyProvider = ({ children }) => {
  const [recommendationStrategy, setRecommendationStrategy] = useState("history");
  const [llmStrategy, setLLMStrategy] = useState("emulator");

  return (
    <StrategyContext.Provider
      value={{
        recommendationStrategy,
        setRecommendationStrategy,
        llmStrategy,
        setLLMStrategy
      }}
    >
      {children}
    </StrategyContext.Provider>
  );
};
