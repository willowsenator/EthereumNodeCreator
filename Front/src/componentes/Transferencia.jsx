import React, { useState } from 'react';
import Web3 from 'web3';
import { Link } from 'react-router-dom';

function Transferencia() {
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');

    const sendTransaction = async () => {
        if (!Web3.utils.isAddress(recipient)) {
            alert('La dirección del destinatario no es válida.');
            return;
        }

        const web3 = new Web3(Web3.givenProvider || "tu-url-rpc");
        try {
            const accounts = await web3.eth.getAccounts();
            const transactionParameters = {
                to: recipient,
                from: accounts[0],
                value: web3.utils.toHex(web3.utils.toWei(amount, 'ether'))
            };

            await web3.eth.sendTransaction(transactionParameters);
            alert('Transacción enviada');
        } catch (error) {
            alert(`Error al enviar la transacción: ${error.message}`);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
                placeholder="Dirección del destinatario"
            />
            <input
                type="text"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Cantidad a enviar"
            />
            <button onClick={sendTransaction}>Enviar Ether</button>
            <div>
                <Link to="/">Volver al Inicio</Link>
            </div>
        </div>
    );
}

export default Transferencia;
