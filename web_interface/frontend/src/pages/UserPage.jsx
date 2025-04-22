import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import {
  getUserById,
  getRecommendations,
  getProductById
} from '../services/api';
import { StrategyContext } from '../context/StrategyContext';

import Carousel from '../components/Carousel';
import ProductCard from '../components/ProductCard';

function UserPage() {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  const { recommendationStrategy } = useContext(StrategyContext);

  useEffect(() => {
    getUserById(id).then(setUser);
  }, [id]);

  const gerarRecomendacoes = async () => {
    setLoading(true);
    try {
      const result = await getRecommendations(id, recommendationStrategy);
      const productIds = (result.recommendations || []).map(r => r.product_id);

      const fullProducts = await Promise.all(productIds.map(getProductById));
      setRecommendations(fullProducts);
    } catch (error) {
      console.error("Erro ao buscar recomendações:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {user && (
        <>
          <h1>{user.name}</h1>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Idade:</strong> {user.age}</p>
          <p><strong>Localização:</strong> {user.location}</p>

          <h2>Preferências</h2>
          <p><strong>Categorias:</strong> {user.preferences.categories.join(', ')}</p>
          <p><strong>Marcas:</strong> {user.preferences.brands.join(', ')}</p>
          <p><strong>Faixa de preço:</strong> {user.preferences.price_range}</p>

          <button className="btn-rounded-left" onClick={gerarRecomendacoes} disabled={loading}>
            {loading ? "Gerando..." : "Gerar Recomendações"}
          </button>

          {recommendations.length > 0 && (
            <Carousel
              title="Recomendados para você"
              items={recommendations}
              renderItem={(p) => <ProductCard product={p} />}
            />
          )}
        </>
      )}
    </div>
  );
}

export default UserPage;
