
import React from 'react';
import { useNavigate } from 'react-router-dom';

function ProductCard({ product }) {
  const navigate = useNavigate();
  return (
    <div className="card" onClick={() => navigate(`/product/${product.id}`)}>
      <h3>{product.name}</h3>
      <p>Categoria: {product.category}</p>
      <p>Preço: R$ {product.price}</p>
    </div>
  );
}

export default ProductCard;
