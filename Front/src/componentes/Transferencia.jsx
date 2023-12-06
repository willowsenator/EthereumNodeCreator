import React, { useState } from 'react';
import Web3 from 'web3';
import { Link } from 'react-router-dom';
import { Button, Form, Alert, Spinner, Row, Col } from 'react-bootstrap';

function Transferencia() {
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const [feedback, setFeedback] = useState({ type: '', message: '' }); // Estado para el feedback

    const sendTransaction = async () => {
        // Antes de intentar enviar, verifica que hay un destinatario y una cantidad
        if (!recipient || !amount) {
        setFeedback({ type: 'error', message: 'Por favor, llena todos los campos.' });
        return;
        }
        
        // Validación de la dirección del destinatario
        if (!Web3.utils.isAddress(recipient)) {
        setFeedback({ type: 'error', message: 'La dirección del destinatario no es válida.' });
        return;
        }

        // Configura el estado de carga y limpia mensajes anteriores
        setLoading(true);
        setFeedback({ type: '', message: '' });

        // Configura tu instancia de Web3, reemplaza "tu-url-rpc" con tu URL de RPC
        const web3 = new Web3(Web3.givenProvider || "tu-url-rpc");
        try {
        // Obtiene las cuentas y envía la transacción
        const accounts = await web3.eth.getAccounts();
        const transactionParameters = {
            to: recipient,
            from: accounts[0],
            value: web3.utils.toHex(web3.utils.toWei(amount, 'ether')),
        };

        await web3.eth.sendTransaction(transactionParameters);
        setFeedback({ type: 'success', message: 'Transacción enviada con éxito.' });
        } catch (error) {
        setFeedback({ type: 'error', message: `Error al enviar la transacción: ${error.message}` });
        } finally {
        setLoading(false);
        }
    };

    return (
        <div className="transferencia-container">
        {feedback.message && (
            <Alert variant={feedback.type === 'error' ? 'danger' : 'success'}>
            {feedback.message}
            </Alert>
        )}
        <Form>
            <Row className="align-items-end">
            <Col xs={12} md={7}>
                <Form.Group>
                <Form.Label>Dirección del destinatario</Form.Label>
                <Form.Control
                    type="text"
                    value={recipient}
                    onChange={(e) => setRecipient(e.target.value)}
                    placeholder="Ingresa la dirección del destinatario"
                    isInvalid={feedback.type === 'error'}
                />
                </Form.Group>
            </Col>
            <Col xs={12} md={3}>
                <Form.Group>
                <Form.Label>Cantidad</Form.Label>
                <Form.Control
                    type="text"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Ingresa la cantidad a enviar"
                />
                </Form.Group>
            </Col>
            <Col xs={12} md={2}>
                <Button variant="primary" onClick={sendTransaction} disabled={loading}>
                {loading ? (
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                ) : (
                    'Enviar Ether'
                )}
                </Button>
            </Col>
            </Row>
        </Form>
        <Link to="/" className="back-link">Volver al Inicio</Link>
        </div>
    );
    }
export default Transferencia;