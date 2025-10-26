import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Classes from './pages/Classes';
import ClassDetail from './pages/ClassDetail';
import './App.css'
import Navbar from "./components/Layout/Navbar.tsx";

function App() {
    return (
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/classes" element={<Classes />} />
                <Route path="/class/:classId" element={<ClassDetail />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App