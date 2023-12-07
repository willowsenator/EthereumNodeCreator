import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from "./Header";
import Body from "./Body";
// import Nodes from "./Nodes";
import Footer from "./Footer";
import Transferencia from './Transferencia'; 
import './styles.css';

export function Home() {
    return (
        <Router>
            <div className="container">
                <Header/>
                {/* Enlace a Transferencia */}
                <nav>
                    <Link to="/transferencia">Ir a Transferencia</Link>
                </nav>
                <Routes>
                    <Route path="/" element={<Body />} />
                    <Route path="/transferencia" element={<Transferencia />} />
                </Routes>
                {/* <Nodes/> */}
                <Footer/>
            </div>
        </Router>
    );
}
