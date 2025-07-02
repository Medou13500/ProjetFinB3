import React from 'react';
import { useNavigate } from 'react-router-dom';

const Accueil = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/Connexion'); // navigation vers la vraie route
  };

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh', width: '100%' }}>
      <div className="d-flex flex-column align-items-center" style={{ width: '1092px' }}>
        <div
          style={{
            width: '100%',
            height: '206px',
            textAlign: 'left',
            fontFamily: 'Inter, sans-serif',
            display: 'flex',
            alignItems: 'flex-start',
          }}
        >
          <p
            className="fw-normal"
            style={{
              fontSize: '30px',
              lineHeight: '100%',
              letterSpacing: '0',
              margin: 0,
            }}
          >
            Bienvenue sur votre tableau de bord administrateur. Ici, vous avez les outils pour
            suivre, gérer et optimiser les performances des utilisateurs. Votre vision, leur
            progression !
          </p>
        </div>

        <button
          onClick={handleClick}
          className="mt-4"
          style={{
            backgroundColor: '#00CFE8',
            color: 'white',
            fontSize: '20px',
            padding: '10px 40px',
            border: 'none',
            borderRadius: '40px',
            cursor: 'pointer',
            width: '300px',
            fontFamily: 'Inter, sans-serif',
          }}
        >
          Connexion
        </button>
      </div>
    </div>
  );
};

export default Accueil;
