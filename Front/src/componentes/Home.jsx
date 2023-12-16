import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from "./Header";
import Footer from "./Footer";
import Transferencia from './Transferencia';
import Body from "./Body";
import imagen1 from '../imagenes/imagen1.png';
import imagen2 from '../imagenes/imagen2.png';
import imagen3 from '../imagenes/imagen3.png';
import './styles.css';

export function Home() {
    // Contenido para la página principal
    const homeContent = (
        <div className="image-links" style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '20px 0' }}>
            <div className="link-container">
                <Link to="/body">
                    <img src={imagen1} alt="Home" style={{ width: '100%', maxWidth: '300px' }} />
                    <p style={{ textAlign: 'center' }}>Inicio</p>
                </Link>
            </div>
            <div className="link-container">
                <Link to="/transferencia">
                    <img src={imagen2} alt="Transferencia" style={{ width: '100%', maxWidth: '300px' }} />
                    <p style={{ textAlign: 'center' }}>Transferencia</p>
                </Link>
            </div>
            <div className="link-container">
                <Link to="/body">
                    <img src={imagen3} alt="NodeCreator" style={{ width: '100%', maxWidth: '300px' }} />
                    <p style={{ textAlign: 'center' }}>Node Creator</p>
                </Link>
            </div>
        </div>
    );

    return (
        <Router>
            <Header/>
            <Routes>
                {/* Ruta para la página de inicio que muestra los enlaces */}
                <Route path="/" element={homeContent} />
                {/* Rutas para las otras páginas */}
                <Route path="/transferencia" element={<Transferencia />} />
                <Route path="/body" element={<Body />} />
                {/* Añade más rutas según sea necesario */}
            </Routes>
            <Footer/>
        </Router>
    );
}
