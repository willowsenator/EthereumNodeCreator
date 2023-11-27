import React from 'react';
import Header from "./Header";
import Body from "./Body";
import Footer from "./Footer";
import './styles.css';



export function Home() {
    return <div className="container">
        <Header/>
        <Body/>
        <Footer/>
    </div>
}

