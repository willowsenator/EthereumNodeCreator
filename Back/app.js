const express = require('express');
const app = express();
const port = 3001;

app.get("/ping", (req, res) => {
    res.send({ fecha: new Date().toISOString() });
});

app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});

module.exports = app;