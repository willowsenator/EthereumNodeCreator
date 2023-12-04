import React, { useState } from 'react';
import './styles.css'; 

function Body() {
  const [networkId, setNetworkId] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Número de Red:', networkId);
  };

  return (
    <div className="body-container">
      <div className="network-form-container">
        <form onSubmit={handleSubmit} className="network-form">
          <div className="form-group">
            <label htmlFor="networkId">Número de Nodos:</label>
            <input
              type="text"
              id="networkId"
              value={networkId}
              onChange={(e) => setNetworkId(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="submit-btn">Crear Red</button>
        </form>
      </div>
    </div>
  );
}

export default Body;
