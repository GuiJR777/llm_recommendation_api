
import React from 'react';
import './Carousel.css';

function Carousel({ title, items, renderItem }) {
  return (
    <div className="carousel">
      <h2>{title}</h2>
      <div className="carousel-track">
        {items.map((item, index) => (
          <div key={index} className="carousel-item">
            {renderItem(item)}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Carousel;
