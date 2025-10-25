import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Chat from './pages/Chat';
import './App.css'
import Navbar from "./components/Layout/Navbar.tsx";

function App() {

    return (
        <BrowserRouter>
                <Navbar />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/chat" element={<Chat />} />
                    </Routes>
        </BrowserRouter>
    )
}

export default App
