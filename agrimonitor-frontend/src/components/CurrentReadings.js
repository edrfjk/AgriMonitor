import React from 'react';

export default function CurrentReadings({ data }) {
    return (
        <div className="current-readings">
            <div className="reading-card temperature">
                <div className="icon">🌡️</div>
                <div className="value">{data.temperature.toFixed(1)}°C</div>
                <div className="label">Temperature</div>
            </div>
            
            <div className="reading-card humidity">
                <div className="icon">💧</div>
                <div className="value">{data.humidity.toFixed(1)}%</div>
                <div className="label">Humidity</div>
            </div>
            
            <div className="reading-card moisture">
                <div className="icon">🌱</div>
                <div className="value">{data.soil_moisture.toFixed(1)}%</div>
                <div className="label">Soil Moisture</div>
            </div>
            
            <div className="reading-card light">
                <div className="icon">☀️</div>
                <div className="value">{data.light_intensity ? Math.round(data.light_intensity) : 'N/A'}</div>
                <div className="label">Light Intensity</div>
            </div>
        </div>
    );
}