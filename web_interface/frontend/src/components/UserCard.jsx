
import React from 'react';
import { useNavigate } from 'react-router-dom';

function UserCard({ user }) {
  const navigate = useNavigate();
  return (
    <div className="card" onClick={() => navigate(`/user/${user.id}`)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <p>{user.location}</p>
    </div>
  );
}

export default UserCard;
