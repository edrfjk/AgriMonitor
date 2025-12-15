import React, { useEffect, useState } from 'react';
import { farms } from '../services/api';
import SensorChart from './SensorChart';
import CurrentReadings from './CurrentReadings';
import Alerts from './Alerts';
import './Dashboard.css';

export default function Dashboard() {
    const [farmList, setFarmList] = useState([]);
    const [selectedFarmId, setSelectedFarmId] = useState(null);
    const [data, setData] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [days, setDays] = useState(7);
    
    useEffect(() => {
        loadFarms();
    }, []);
    
    const loadFarms = async () => {
        try {
            const response = await farms.list();
            if (response.data.length > 0) {
                setFarmList(response.data);
                setSelectedFarmId(response.data[0].id);
            }
        } catch (err) {
            console.error('Failed to load farms', err);
        }
    };
    
    useEffect(() => {
        if (selectedFarmId) {
            loadData();
        }
    }, [selectedFarmId, days]);
    
    const loadData = async () => {
        setLoading(true);
        try {
            const [dataRes, alertsRes] = await Promise.all([
                farms.getData(selectedFarmId, days),
                farms.getAlerts(selectedFarmId)
            ]);
            
            setData(dataRes.data);
            setAlerts(alertsRes.data);
        } catch (err) {
            console.error('Failed to load data', err);
        } finally {
            setLoading(false);
        }
    };
    
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('email');
        window.location.reload();
    };
    
    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>🌱 AgriMonitor Dashboard</h1>
                <button onClick={handleLogout} className="logout-btn">
                    Logout
                </button>
            </header>
            
            <div className="dashboard-content">
                {/* Farm selector */}
                <div className="farm-selector">
                    <label>Select Farm:</label>
                    <select
                        value={selectedFarmId || ''}
                        onChange={(e) => setSelectedFarmId(parseInt(e.target.value))}
                    >
                        {farmList.map(farm => (
                            <option key={farm.id} value={farm.id}>
                                {farm.name} ({farm.crop_type})
                            </option>
                        ))}
                    </select>
                </div>
                
                {/* Time range selector */}
                <div className="time-selector">
                    <label>Time Range:</label>
                    <button
                        className={days === 1 ? 'active' : ''}
                        onClick={() => setDays(1)}
                    >
                        24h
                    </button>
                    <button
                        className={days === 7 ? 'active' : ''}
                        onClick={() => setDays(7)}
                    >
                        7d
                    </button>
                    <button
                        className={days === 30 ? 'active' : ''}
                        onClick={() => setDays(30)}
                    >
                        30d
                    </button>
                </div>
                
                {loading ? (
                    <p className="loading">⏳ Loading data...</p>
                ) : (
                    <>
                        {data.length > 0 ? (
                            <>
                                <CurrentReadings data={data[0]} />
                                <SensorChart data={data} />
                            </>
                        ) : (
                            <p className="no-data">No data available</p>
                        )}
                        
                        {alerts.length > 0 && <Alerts alerts={alerts} />}
                    </>
                )}
                
                <button onClick={loadData} className="btn-refresh">
                    🔄 Refresh Now
                </button>
            </div>
        </div>
    );
}