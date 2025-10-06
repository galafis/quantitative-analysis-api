import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def generate_sample_data(days=30):
    """Generate sample price data"""
    base_date = datetime.now() - timedelta(days=days)
    data = []
    price = 100.0
    
    for i in range(days):
        price *= (1 + (0.02 * (0.5 - abs(hash(i) % 100) / 100)))
        data.append({
            "timestamp": (base_date + timedelta(days=i)).isoformat(),
            "open": price,
            "high": price * 1.02,
            "low": price * 0.98,
            "close": price,
            "volume": 1000000.0
        })
    
    return data

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_sma_calculation():
    data = generate_sample_data(50)
    request_data = {
        "symbol": "TEST",
        "data": data
    }
    
    response = client.post("/indicators/sma?period=20", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert result["symbol"] == "TEST"
    assert result["indicator"] == "SMA_20"
    assert len(result["values"]) == 50

def test_rsi_calculation():
    data = generate_sample_data(50)
    request_data = {
        "symbol": "TEST",
        "data": data
    }
    
    response = client.post("/indicators/rsi?period=14", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert result["symbol"] == "TEST"
    assert result["indicator"] == "RSI_14"

def test_statistics_summary():
    data = generate_sample_data(100)
    request_data = {
        "symbol": "TEST",
        "data": data
    }
    
    response = client.post("/statistics/summary", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "sharpe_ratio" in result
    assert "volatility" in result
    assert "max_drawdown" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
