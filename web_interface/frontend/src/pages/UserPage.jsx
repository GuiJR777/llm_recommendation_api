
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getUserById, getProductById, getRecommendations } from '../services/api';
import Carousel from '../components/Carousel';
import ProductCard from '../components/ProductCard';

function UserPage() {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    getUserById(id).then(setUser);
  }, [id]);

  useEffect(() => {
    if (user) {
      const productIds = [
        ...user.purchase_history.map(p => p.product_id),
        ...user.browsing_history.map(p => p.product_id),
        ...user.cart_events.map(p => p.product_id)
      ];
      const unique = [...new Set(productIds)];
      Promise.all(unique.map(getProductById)).then(setProducts);
    }
  }, [user]);

  const gerarRecomendacoes = () => {
    getRecommendations(id).then(setRecommendations);
  };

  return (
    <div className="container">
      {user && <>
        <h1>{user.name}</h1>
        <p>Email: {user.email}</p>
        <p>Localização: {user.location}</p>

        <Carousel title="Histórico de Compras / Navegação / Carrinho" items={products} renderItem={(p) => <ProductCard product={p} />} />

        <button onClick={gerarRecomendacoes}>Gerar Recomendações</button>

        {recommendations.length > 0 && (
          <Carousel title="Recomendados para você" items={recommendations} renderItem={(p) => <ProductCard product={p} />} />
        )}
      </>}
    </div>
  );
}

export default UserPage;
