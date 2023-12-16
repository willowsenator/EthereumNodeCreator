import React, { useState } from 'react';
import Web3 from 'web3';
import { Link } from 'react-router-dom';

function Transferencia() {
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');

    const sendTransaction = async () => {
        // ... tu lógica de envío de transacciones
    };

    return (
        <div className="transfer-container">
            <h2>Enviar Ether</h2>
            <div className="input-group">
                <label htmlFor="recipient">Dirección del destinatario:</label>
                <input
                    id="recipient"
                    type="text"
                    value={recipient}
                    onChange={(e) => setRecipient(e.target.value)}
                    placeholder="Dirección del destinatario"
                />
            </div>
            <div className="input-group">
                <label htmlFor="amount">Cantidad a enviar (ETH):</label>
                <input
                    id="amount"
                    type="text"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Cantidad a enviar"
                />
            </div>
            <button className="send-button" onClick={sendTransaction}>Enviar Ether</button>
            <Link to="/" className="back-link">Volver al Inicio</Link>
        </div>
    );
}

export default Transferencia;
