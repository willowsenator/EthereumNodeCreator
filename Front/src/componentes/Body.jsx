import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

function Body() {
  const [networkId, setNetworkId] = useState('');
  const [nodes, setNodes] = useState([]);

  useEffect(() => {
    // Realiza la solicitud para obtener los nodos desde el servidor
    axios.get('/api/nodos')
      .then(response => setNodes(response.data))
      .catch(error => console.error('Error al obtener nodos:', error));
  }, []); // El segundo parámetro es un arreglo vacío, ejecuta el efecto solo una vez al montar el componente

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Número de Nodos:', networkId);
    // Realiza la solicitud para insertar un nuevo nodo
    try {
      await axios.post('/api/insertar', { nombre: 'Nombre Ejemplo', numeroRed: networkId });
      // Actualiza la lista de nodos después de la inserción
      // Puedes también recargar toda la página o manejarlo de manera más eficiente
      // dependiendo de tu aplicación
      // Aquí simplemente recargamos la página entera
      window.location.reload();
    } catch (error) {
      console.error('Error al insertar nodo:', error);
    }
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
      <div className="node-list-container">
        <h2>Listado de Nodos</h2>
        <ul>
          {nodes.map(node => (
            <li key={node.id}>{node.name_node} - Red: {node.n_red}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Body;
