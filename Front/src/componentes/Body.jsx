import React, { useState } from 'react';
import axios from 'axios';
import './styles.css';

function Body() {
  const [networkId, setNetworkId] = useState('');
  const [redId, setRedId] = useState('');
  const [rpcNodeId, setRpcNodeId] = useState('');
  const [minerNodeId, setMinerNodeId] = useState('');
  const [normalNodeId, setNormalNodeId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Aquí, en lugar de una llamada a la API, se manejaría toda la lógica para crear la red con los nodos.
    try {
      const response = await axios.post('/api/create-network', {
        networkId,
        redId,
        nodes: [
          { id: rpcNodeId, type: 'RPC' },
          { id: minerNodeId, type: 'Minero' },
          { id: normalNodeId, type: 'Normal' }
        ]
      });
      console.log(response.data);
      // Manejo post-creación de la red...
    } catch (error) {
      console.error('Hubo un error al crear la red:', error);
      // Manejo del error...
    }
  };

  return (
    <div className="body-container">
      <form onSubmit={handleSubmit} className="network-form">
        <div className="form-group"/>
      
        <div className="form-group">
          <label htmlFor="redId">Id Red:</label>
          <input
            type="text"
            id="redId"
            value={redId}
            onChange={(e) => setRedId(e.target.value)}
            className="input-field"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="rpcNodeId"> Nodos RPC:</label>
          <input
            type="text"
            id="rpcNodeId"
            value={rpcNodeId}
            onChange={(e) => setRpcNodeId(e.target.value)}
            className="input-field"
          />
        </div>
        <div className="form-group">
          <label htmlFor="minerNodeId">Nodos Mineros:</label>
          <input
            type="text"
            id="minerNodeId"
            value={minerNodeId}
            onChange={(e) => setMinerNodeId(e.target.value)}
            className="input-field"
          />
        </div>
        <div className="form-group">
          <label htmlFor="normalNodeId">Nodos Normales:</label>
          <input
            type="text"
            id="normalNodeId"
            value={normalNodeId}
            onChange={(e) => setNormalNodeId(e.target.value)}
            className="input-field"
          />
        </div>
        <button type="submit" className="submit-btn">Crear Red</button>
      </form>
    
    </div>
  );
}

export default Body;
