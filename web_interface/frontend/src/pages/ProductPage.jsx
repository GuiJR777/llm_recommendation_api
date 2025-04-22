
import React, { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { getProductById, getProductDescription } from '../services/api';

function ProductPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [description, setDescription] = useState('');
  const location = useLocation();
  const userId = new URLSearchParams(location.search).get("user_id");

  useEffect(() => {
    getProductById(id).then(setProduct);
    getProductDescription(id, userId).then(setDescription);
  }, [id]);

  return (
    <div className="container">
      {product && <>
        <h1>{product.name}</h1>
        <p>Categoria: {product.category}</p>
        <p>Marca: {product.brand}</p>
        <p>Preço: R$ {product.price}</p>
        <p><strong>Descrição:</strong> {description}</p>
      </>}
    </div>
  );
}

export default ProductPage;
