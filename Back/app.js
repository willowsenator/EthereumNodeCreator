const express = require("express")
const app = express();

app.get("/ping", async (req, res) => {
    res.send({ fecha: new Date().toISOString()})
})

app.listen(3001, () => {
    console.log("listening")
})

app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
  });   