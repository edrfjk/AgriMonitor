import React, { useState } from 'react';
import { auth } from '../services/api';
import './Login.css';

export default function Login({ onLoginSuccess }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);
    const [loading, setLoading] = useState(false);
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        
        try {
            const response = isRegistering
                ? await auth.register(email, password)
                : await auth.login(email, password);
            
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('email', response.data.email);
            
            onLoginSuccess();
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="login-container">
            <div className="login-card">
                <h1>🌱 AgriMonitor</h1>
                <p className="subtitle">Smart Agriculture Monitoring</p>
                
                <form onSubmit={handleSubmit}>
                    <h2>{isRegistering ? 'Create Account' : 'Login'}</h2>
                    
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        disabled={loading}
                    />
                    
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                    />
                    
                    {error && <p className="error">❌ {error}</p>}
                    
                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? 'Loading...' : (isRegistering ? 'Register' : 'Login')}
                    </button>
                </form>
                
                <p className="toggle-auth">
                    {isRegistering ? 'Already have account?' : "Don't have account?"}{' '}
                    <button
                        type="button"
                        onClick={() => {
                            setIsRegistering(!isRegistering);
                            setError('');
                        }}
                        className="link-btn"
                    >
                        {isRegistering ? 'Login' : 'Register'}
                    </button>
                </p>
                
                <div className="demo-hint">
                    <p><strong>Demo Credentials:</strong></p>
                    <p>Email: demo@example.com</p>
                    <p>Password: demo123</p>
                </div>
            </div>
        </div>
    );
}