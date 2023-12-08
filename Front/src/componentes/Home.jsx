import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from "./Header";
import Body from "./Body";
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
                
                    <Link className="link-style" to="/transferencia">Transferencia</Link>
                    <Link className="link-style" to="/NodeCreator">NodeCreator</Link>
                    <Link className="link-style" to="/Explorador">Explorador</Link>
                </nav>
                <Routes>
                    <Route path="/NodeCreator" element={<Body />} />
                    <Route path="/transferencia" element={<Transferencia />} />
                </Routes>
                <Footer/>
            </div>
        </Router>
    );
}
