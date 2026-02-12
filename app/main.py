"""
Quantitative Analysis API
A FastAPI-based microservice for financial time series analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime

app = FastAPI(
    title="Quantitative Analysis API",
    description="Microservice for financial time series analysis and technical indicators",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PriceData(BaseModel):
    timestamp: datetime
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)

class TimeSeriesRequest(BaseModel):
    symbol: str
    data: List[PriceData]

class IndicatorResponse(BaseModel):
    symbol: str
    indicator: str
    values: List[float]
    timestamps: List[datetime]

class StatisticsResponse(BaseModel):
    symbol: str
    mean_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    total_return: float

# Technical Indicators
class TechnicalIndicators:
    @staticmethod
    def sma(prices: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    @staticmethod
    def ema(prices: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average"""
        return prices.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        """MACD Indicator"""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0):
        """Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band

# Statistical Analysis
class StatisticalAnalysis:
    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """Calculate percentage returns"""
        return prices.pct_change()
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
        """Calculate volatility (standard deviation of returns)"""
        vol = returns.std()
        if annualize:
            vol *= np.sqrt(252)  # Annualize assuming 252 trading days
        return float(vol)
    
    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio"""
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = returns.std() * np.sqrt(252)
        if volatility == 0:
            return 0.0
        return float(excess_returns / volatility)
    
    @staticmethod
    def calculate_max_drawdown(prices: pd.Series) -> float:
        """Calculate maximum drawdown"""
        cumulative = (1 + prices.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return float(drawdown.min())
    
    @staticmethod
    def calculate_correlation(series1: pd.Series, series2: pd.Series) -> float:
        """Calculate correlation between two series"""
        return float(series1.corr(series2))

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Quantitative Analysis API",
        "version": "1.0.0",
        "endpoints": [
            "/indicators/sma",
            "/indicators/ema",
            "/indicators/rsi",
            "/indicators/macd",
            "/indicators/bollinger",
            "/statistics/summary",
            "/statistics/correlation"
        ]
    }

@app.post("/indicators/sma", response_model=IndicatorResponse)
async def calculate_sma(request: TimeSeriesRequest, period: int = 20):
    """Calculate Simple Moving Average"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    sma_values = TechnicalIndicators.sma(df['close'], period)
    
    return IndicatorResponse(
        symbol=request.symbol,
        indicator=f"SMA_{period}",
        values=sma_values.fillna(0).tolist(),
        timestamps=df['timestamp'].tolist()
    )

@app.post("/indicators/ema", response_model=IndicatorResponse)
async def calculate_ema(request: TimeSeriesRequest, period: int = 20):
    """Calculate Exponential Moving Average"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    ema_values = TechnicalIndicators.ema(df['close'], period)
    
    return IndicatorResponse(
        symbol=request.symbol,
        indicator=f"EMA_{period}",
        values=ema_values.fillna(0).tolist(),
        timestamps=df['timestamp'].tolist()
    )

@app.post("/indicators/rsi", response_model=IndicatorResponse)
async def calculate_rsi(request: TimeSeriesRequest, period: int = 14):
    """Calculate Relative Strength Index"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    rsi_values = TechnicalIndicators.rsi(df['close'], period)
    
    return IndicatorResponse(
        symbol=request.symbol,
        indicator=f"RSI_{period}",
        values=rsi_values.fillna(0).tolist(),
        timestamps=df['timestamp'].tolist()
    )

@app.post("/indicators/macd")
async def calculate_macd(request: TimeSeriesRequest, fast: int = 12, slow: int = 26, signal: int = 9):
    """Calculate MACD"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    macd_line, signal_line, histogram = TechnicalIndicators.macd(df['close'], fast, slow, signal)
    
    return {
        "symbol": request.symbol,
        "indicator": "MACD",
        "macd_line": macd_line.fillna(0).tolist(),
        "signal_line": signal_line.fillna(0).tolist(),
        "histogram": histogram.fillna(0).tolist(),
        "timestamps": df['timestamp'].tolist()
    }

@app.post("/indicators/bollinger")
async def calculate_bollinger(request: TimeSeriesRequest, period: int = 20, std_dev: float = 2.0):
    """Calculate Bollinger Bands"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    upper, middle, lower = TechnicalIndicators.bollinger_bands(df['close'], period, std_dev)
    
    return {
        "symbol": request.symbol,
        "indicator": "Bollinger Bands",
        "upper_band": upper.fillna(0).tolist(),
        "middle_band": middle.fillna(0).tolist(),
        "lower_band": lower.fillna(0).tolist(),
        "timestamps": df['timestamp'].tolist()
    }

@app.post("/statistics/summary", response_model=StatisticsResponse)
async def calculate_statistics(request: TimeSeriesRequest):
    """Calculate comprehensive statistics"""
    df = pd.DataFrame([d.model_dump() for d in request.data])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    returns = StatisticalAnalysis.calculate_returns(df['close'])
    
    return StatisticsResponse(
        symbol=request.symbol,
        mean_return=float(returns.mean() * 252),  # Annualized
        volatility=StatisticalAnalysis.calculate_volatility(returns),
        sharpe_ratio=StatisticalAnalysis.calculate_sharpe_ratio(returns),
        max_drawdown=StatisticalAnalysis.calculate_max_drawdown(df['close']),
        total_return=float((df['close'].iloc[-1] / df['close'].iloc[0]) - 1)
    )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
