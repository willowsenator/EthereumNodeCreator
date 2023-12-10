// Importa las dependencias necesarias
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Componente para mostrar el listado
function NodeList() {
  const [nodes, setNodes] = useState([]);

  useEffect(() => {
    // Realiza la solicitud para obtener los nodos desde el servidor
    axios.get('/api/nodos')
      .then(response => setNodes(response.data))
      .catch(error => console.error('Error al obtener nodos:', error));
  }, []); // El segundo parámetro es un arreglo vacío, ejecuta el efecto solo una vez al montar el componente

  return (
    <div>
      <h2>Listado de Nodos</h2>
      <ul>
        {nodes.map(node => (
          <li key={node.id}>{node.name_node} - Red: {node.n_red}</li>
        ))}
      </ul>
    </div>
  );
}

// Componente para el formulario de mantenimiento
function NodeForm() {
  const [nombre, setNombre] = useState('');
  const [numeroRed, setNumeroRed] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Realiza la solicitud para insertar un nuevo nodo
    try {
      await axios.post('/api/insertar', { nombre, numeroRed });
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
    <div>
      <h2>Formulario de Mantenimiento</h2>
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Insertar Nodo</button>
      </form>
    </div>
  );
}

// Componente principal que engloba NodeList y NodeForm
function App() {
  return (
    <div>
      <NodeList />
      <NodeForm />
    </div>
  );
}

export default App;



// import React, { useState } from 'react';
// import axios from 'axios';
// import { useQuery } from 'react-query';
// import { Link } from 'react-router-dom';


// const FormularioBD = () => {
//   const [nombre, setNombre] = useState('');
//   const [numeroRed, setNumeroRed] = useState('');

//   const handleInsertar = async () => {
//     try {
//       // Llamada al backend para insertar en la base de datos
//       await axios.post('/api/insertar', { nombre, numeroRed });
//       // Actualizar interfaz o mostrar mensaje de éxito
//     } catch (error) {
//       console.error('Error al insertar registro', error);
//     }
//   };

//   const handleEliminar = async () => {
//     try {
//       // Llamada al backend para eliminar 
//       await axios.delete('/api/eliminar', { data: { nombre } });
//       // Actualizar interfaz o mostrar mensaje de éxito
//     } catch (error) {
//       console.error('Error al eliminar registro', error);
//     }
//   };

//   const handleModificar = async () => {
//     try {
//       // Llamada al backend para modificar en la base de datos
//       await axios.put('/api/modificar', { nombre, numeroRed });
//       // Actualizar interfaz o mostrar mensaje de éxito
//     } catch (error) {
//       console.error('Error al modificar registro', error);
//     }
//   };

//   return (
//     <div>
//       <label>
//         Nombre: 
//         <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} />
//       </label>
//       <br />
//       <label>
//         Número de Red: 
//         <input type="text" value={numeroRed} onChange={(e) => setNumeroRed(e.target.value)} />
//       </label>
//       <br />
//       <button type="submit" className="submit-btn" onClick={handleInsertar}>Insertar</button>
//       <button type="submit" className="submit-btn" onClick={handleEliminar}>Eliminar</button>
//       <button type="submit" className="submit-btn" onClick={handleModificar}>Modificar</button>

//       {/* <button type="submit" className="submit-btn">Crear Red</button> */}
//     </div>
//   );
// };

// export default FormularioBD;