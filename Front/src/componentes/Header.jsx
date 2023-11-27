import {Logo} from './Logo'

export function Header() {
    return (
        <div className="d-flex" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div className="d-flex" style={{ alignItems: 'center' }}>
                <Logo></Logo>
                <p style={{ marginTop: '0.5rem' }}>Build Private Ethereum Network</p>
            </div>
        </div>
    );
}
