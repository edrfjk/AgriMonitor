import React from 'react';

export default function Alerts({ alerts }) {
    if (!alerts || alerts.length === 0) {
        return (
            <div className="alerts-container">
                <h2>⏲️ Alerts</h2>
                <p>✅ No alerts - All systems normal!</p>
            </div>
        );
    }
    
    return (
        <div className="alerts-container">
            <h2>⚠️ Alerts ({alerts.length})</h2>
            {alerts.map((alert, index) => (
                <div key={index} className={`alert alert-${alert.alert_type}`}>
                    <strong>{alert.alert_type.replace(/_/g, ' ').toUpperCase()}</strong>
                    <p>{alert.message}</p>
                    <small>{new Date(alert.created_at).toLocaleString()}</small>
                </div>
            ))}
        </div>
    );
}