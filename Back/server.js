// server.js

const express = require('express');
const { Pool } = require('pg');
const db = require('./config'); 

const app = express();
const port = 3001;

 const pool = new Pool(db);

app.use(express.json());

// Ruta para insertar un registro
app.get('/api/nodos', async (req, res) => {
  try {
      const [results, fields] = await db.q('SELECT id, name_node, n_red FROM PUBLIC.NODES WHERE node_active = true');
      res.send(results);
  } catch (error) {
      console.error('Error en la consulta:', error);
      res.status(500).send({ error: 'Error en la consulta a la bd.' });
  }
});


// Ruta para insertar un registro
app.get('/api/nodo', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await db.q('SELECT id, name_node, n_red FROM PUBLIC.NODES WHERE node_active = true AND id = $1',[req.params.id]);
    res.send(result);
  } catch (error) {
    console.log();
    console.error('Error al insertar en la base de datos', error);
    res.status(500).json({ error: 'Error en la consulta a la base de datos' });
  }
});

// Ruta para insertar un registro
app.post('/api/insertar', async (req, res) => {
  const { nombre, numeroRed } = req.body;

  try {
    const result = await db.q('INSERT INTO PUBLIC.NODES (name_node, n_red, category, date_creation, node_active, updated) VALUES ($1, $2, $3, $4, 1, $6)', [nombre, numeroRed]);
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
    const result = await db.q('UPDATE PUBLIC.NODES SET date_deleted=now(), node_active=false, updated=true WHERE id = $1', [nombre]);
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
    const result = await db.q('UPDATE PUBLIC.NODES SET name_node=$2, n_red=$3, category=0, node_active=false, updated=false WHERE id = $1', [numeroRed, nombre]);
    res.json({ message: 'Registro modificado correctamente' });
  } catch (error) {
    console.error('Error al modificar en la base de datos', error);
    res.status(500).json({ error: 'Error al modificar en la base de datos' });
  }
});

app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});     

const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

//EndPoint creacion de la red
app.post('/ejecutar-python', (req, res) => {
    // Ejecutar el script de Python
    exec('python generate_network.py -network_id, -num_rpc_nodes, -num_miner_nodes ', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error al ejecutar el script: ${error}`);
            res.status(500).send('Error interno del servidor');
            return;
        }

        console.log(`Resultado del script: ${stdout}`);
        res.send(`Resultado del script: ${stdout}`);
    });
});

app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});
