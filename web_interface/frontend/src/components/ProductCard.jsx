import React from 'react';
import { useNavigate } from 'react-router-dom';

function ProductCard({ product }) {
  const navigate = useNavigate();

  return (
    <div className="card-tooltip-wrapper">
      <div className="card" onClick={() => navigate(`/product/${product.id}`)}>
        <h3>{product.name}</h3>
        <p>Categoria: {product.category}</p>
        <p><strong>R$ {product.price?.toFixed(2)}</strong></p>
      </div>
      <div className="card-tooltip">Clique para gerar descrição</div>
    </div>
  );
}

export default ProductCard;
