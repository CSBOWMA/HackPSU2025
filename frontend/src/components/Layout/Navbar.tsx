import { Link } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-brand">
                <h2>My App</h2>
            </div>
            <ul className="nav-links">
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/chat">Chat</Link>
                </li>
                <li>
                    <Link to="/classes">Classes</Link>
                </li>
            </ul>
        </nav>
    );
}