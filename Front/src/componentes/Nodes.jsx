import React, { useState } from 'react';
import axios from 'axios';

const FormularioBD = () => {
  const [nombre, setNombre] = useState('');
  const [numeroRed, setNumeroRed] = useState('');

  const handleInsertar = async () => {
    try {
      // Llamada al backend para insertar en la base de datos
      await axios.post('/api/insertar', { nombre, numeroRed });
      // Actualizar interfaz o mostrar mensaje de éxito
    } catch (error) {
      console.error('Error al insertar en la base de datos', error);
    }
  };

  const handleEliminar = async () => {
    try {
      // Llamada al backend para eliminar de la base de datos
      await axios.delete('/api/eliminar', { data: { nombre } });
      // Actualizar interfaz o mostrar mensaje de éxito
    } catch (error) {
      console.error('Error al eliminar de la base de datos', error);
    }
  };

  const handleModificar = async () => {
    try {
      // Llamada al backend para modificar en la base de datos
      await axios.put('/api/modificar', { nombre, numeroRed });
      // Actualizar interfaz o mostrar mensaje de éxito
    } catch (error) {
      console.error('Error al modificar en la base de datos', error);
    }
  };

  return (
    <div>
      <label>
        Nombre:
        <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} />
      </label>
      <br />
      <label>
        Número de Red:
        <input type="text" value={numeroRed} onChange={(e) => setNumeroRed(e.target.value)} />
      </label>
      <br />
      <button onClick={handleInsertar}>Insertar</button>
      <button onClick={handleEliminar}>Eliminar</button>
      <button onClick={handleModificar}>Modificar</button>
    </div>
  );
};

export default FormularioBD;