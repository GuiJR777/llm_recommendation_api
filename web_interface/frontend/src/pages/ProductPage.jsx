import React, { useEffect, useState, useContext } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { getProductById, getProductDescription } from '../services/api';
import { StrategyContext } from '../context/StrategyContext';

function ProductPage() {
  const { id } = useParams();
  const location = useLocation();
  const userId = new URLSearchParams(location.search).get("user_id");

  const [product, setProduct] = useState(null);
  const [description, setDescription] = useState('');

  const { llmStrategy } = useContext(StrategyContext);

  useEffect(() => {
    getProductById(id).then(setProduct);
    getProductDescription(id, userId, llmStrategy).then(setDescription);
  }, [id, userId, llmStrategy]);

  return (
    <div className="container">
      {product && (
        <>
          <h1>{product.name}</h1>
          <p>Categoria: {product.category}</p>
          <p>Marca: {product.brand}</p>
          <p>Preço: R$ {product.price?.toFixed(2)}</p>
          <p><strong>Descrição:</strong> {description}</p>
        </>
      )}
    </div>
  );
}

export default ProductPage;
