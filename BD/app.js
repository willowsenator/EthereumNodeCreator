// app.js
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware para analizar el cuerpo de las solicitudes como JSON
app.use(bodyParser.json());

// Endpoint para manejar transacciones
app.post('/transactions', (req, res) => {
  // Aquí puedes manejar la lógica de la transacción
  // Accede a los datos de la transacción desde req.body

  const { amount, description } = req.body;

  // Ejemplo de lógica simple: solo imprime los datos de la transacción
  console.log('Nueva transacción:');
  console.log('Monto:', amount);
  console.log('Descripción:', description);

  // Puedes realizar operaciones de base de datos, integraciones externas, etc.

  // Responde con un mensaje de éxito
  res.status(200).json({ message: 'Transacción completada exitosamente' });
});

// Inicia el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});