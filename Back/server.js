// yarn init -y
// yarn add express
// yarn add pg

const express = require('express');
const { Pool } = require('pg');
const config = require('./config'); 

const app = express();
const port = 3001;

// const pool = new Pool({
//   user: 'tu_usuario', // Reemplaza con tu nombre de usuario de PostgreSQL
//   host: 'localhost',
//   database: 'tu_base_de_datos', // Reemplaza con el nombre de tu base de datos
//   password: 'tu_contraseña', // Reemplaza con tu contraseña de PostgreSQL
//   port: 5432,
// });

const pool = new Pool(config);

app.use(express.json());

// Ruta para insertar un registro
app.post('/api/nodos', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await pool.query('SELECT id, name_node, n_red FROM public.nodes WHERE node_active = 1');
    res.send(result);
  } catch (error) {
    console.error('Error al insertar en la base de datos', error);
    res.status(500).json({ error: 'Error en la consulta a la base de datos' });
  }
});

// Ruta para insertar un registro
app.post('/api/nodo', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await pool.query('SELECT id, name_node, n_red FROM public.nodes WHERE node_active = 1 AND id = $1',[req.params.id]);
    res.send(result);
  } catch (error) {
    console.error('Error al insertar en la base de datos', error);
    res.status(500).json({ error: 'Error en la consulta a la base de datos' });
  }
});

// Ruta para insertar un registro
app.post('/api/insertar', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await pool.query('INSERT INTO public.nodes (name_node, n_red, category, date_creation, node_active, updated) VALUES ($1, $2, $3, $4, 1, $6)', [nombre, numeroRed]);
    res.json({ message: 'Registro insertado correctamente' });
  } catch (error) {
    console.error('Error al insertar en la base de datos', error);
    res.status(500).json({ error: 'Error al insertar en la base de datos' });
  }
});


// Ruta para eliminar un registro
app.delete('/api/eliminar', async (req, res) => {
  const { nombre } = req.body;

  try {
    const result = await pool.query('UPDATE public.nodes SET date_deleted=now(), node_active=false, updated=true WHERE id = $1', [nombre]);
    res.json({ message: 'Registro eliminado correctamente' });
  } catch (error) {
    console.error('Error al eliminar de la base de datos', error);
    res.status(500).json({ error: 'Error al eliminar de la base de datos' });
  }
});

// Ruta para modificar un registro
app.put('/api/modificar', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await pool.query('UPDATE public.nodes SET name_node=$2, n_red=$3, category=0, node_active=false, updated=false WHERE id = $1', [numeroRed, nombre]);
    res.json({ message: 'Registro modificado correctamente' });
  } catch (error) {
    console.error('Error al modificar en la base de datos', error);
    res.status(500).json({ error: 'Error al modificar en la base de datos' });
  }
});

app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});     