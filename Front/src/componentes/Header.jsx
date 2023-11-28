import {Logo} from './Logo'
import React from 'react';

function Header() {
  return (
    <header>
        <div className="header-content">
        <div className="left-side">
          <h1>Team 4</h1>
        </div>
        <div className="d-flex" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div className="d-flex" style={{ alignItems: 'center' }}>
                <Logo></Logo>
                <p style={{ marginTop: '0.5rem' }}>Build Private Ethereum Network</p>
            </div>
        </div>
      </div>  


    </header>
  );
}

export default Header;