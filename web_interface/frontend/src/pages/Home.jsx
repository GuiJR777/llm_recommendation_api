
import React, { useEffect, useState } from 'react';
import { getAllUsers, getAllProducts } from '../services/api';
import Carousel from '../components/Carousel';
import UserCard from '../components/UserCard';
import ProductCard from '../components/ProductCard';

function Home() {
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    getAllUsers().then(setUsers);
    getAllProducts().then(setProducts);
  }, []);

  return (
    <div className="container">
      <h1>Início</h1>
      <Carousel title="Usuários" items={users} renderItem={(u) => <UserCard user={u} />} />
      <Carousel title="Produtos" items={products} renderItem={(p) => <ProductCard product={p} />} />
    </div>
  );
}

export default Home;
