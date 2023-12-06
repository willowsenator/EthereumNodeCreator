import React, { useState } from 'react';
import './styles.css'; 

function Body() {
  const [nombre, setNombre] = useState('');
  const [numeroRed, setNumeroRed] = useState('');
  const [numeroNodos, setNumeroNodos] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Nombre:', nombre, 'Número de Red:', numeroRed, 'Número de Nodos:', numeroNodos);
    // agregar lógica para interactuar con una API o base de datos
  };

  return (
      <div className="body-container">
        <div className="network-form-container">
          <form onSubmit={handleSubmit} className="network-form">
            <div className="form-group">
              <label htmlFor="nombre">Nombre:</label>
              <input
                type="text"
                id="nombre"
                // ... tus otros atributos ...
              />
            </div>
            <div className="form-group">
              <label htmlFor="numeroRed">Número de Red:</label>
              <input
                type="text"
                id="numeroRed"
                // ... tus otros atributos ...
              />
            </div>
            <div className="form-group">
              <label htmlFor="numeroNodos">Número de Nodos:</label>
              <input
                type="text"
                id="numeroNodos"
                // ... tus otros atributos ...
              />
            </div>
            <button type="submit" className="submit-btn">Crear Red</button>
          </form>
        </div>
      </div>
    );
  }
  


export default Body;

