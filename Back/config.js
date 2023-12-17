// config.js

const { Pool } = require("pg");
const pool = new Pool({
    user: "ether",
    password: "softclaw",
    database: "ETHEREUM_NODES",
    host: "localhost",
    port: 5432
});

    function q(sql, parametros) {
    return new Promise((resolve, reject) => {
        pool.query(sql, parametros, (err, results, fields) => {
            if (err) {
                console.error('Error en la consulta SQL:', err);
                reject({ error: 'Error en la consulta SQL.' });
                return;
            }
            resolve([results, fields]);
        });
    });
    }


module.exports = {
    q
  };