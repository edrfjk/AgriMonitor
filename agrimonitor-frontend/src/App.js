import React, { useState } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(
        !!localStorage.getItem('access_token')
    );
    
    return (
        <div className="App">
            {isLoggedIn ? (
                <Dashboard />
            ) : (
                <Login onLoginSuccess={() => setIsLoggedIn(true)} />
            )}
        </div>
    );
}

export default App;