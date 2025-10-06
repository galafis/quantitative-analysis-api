# 📊 Quantitative Analysis API

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [Português](#português)

---

## English

### Overview

A high-performance FastAPI-based microservice for financial time series analysis, technical indicators calculation, and quantitative statistics. Designed for integration with trading platforms and analytical tools.

### Key Features

- **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands
- **Statistical Analysis**: Sharpe ratio, volatility, max drawdown, correlation
- **RESTful API**: Clean, documented endpoints with OpenAPI/Swagger
- **Redis Caching**: Optional caching for improved performance
- **Async Processing**: Non-blocking I/O with FastAPI
- **Type Safety**: Pydantic models for request/response validation
- **Comprehensive Tests**: pytest-based test suite

### Installation

```bash
# Clone repository
git clone https://github.com/gabriellafis/quantitative-analysis-api.git
cd quantitative-analysis-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Start the API server
uvicorn app.main:app --reload

# Access interactive documentation
# http://localhost:8000/docs
```

### API Endpoints

#### Technical Indicators

**Simple Moving Average (SMA)**
```bash
POST /indicators/sma?period=20
Content-Type: application/json

{
  "symbol": "BTCUSD",
  "data": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "open": 100.0,
      "high": 105.0,
      "low": 98.0,
      "close": 102.0,
      "volume": 1000000.0
    }
  ]
}
```

**Relative Strength Index (RSI)**
```bash
POST /indicators/rsi?period=14
```

**MACD**
```bash
POST /indicators/macd?fast=12&slow=26&signal=9
```

**Bollinger Bands**
```bash
POST /indicators/bollinger?period=20&std_dev=2.0
```

#### Statistical Analysis

**Comprehensive Statistics**
```bash
POST /statistics/summary

Response:
{
  "symbol": "BTCUSD",
  "mean_return": 0.15,
  "volatility": 0.25,
  "sharpe_ratio": 1.2,
  "max_drawdown": -0.18,
  "total_return": 0.45
}
```

### Python Client Example

```python
import requests
from datetime import datetime, timedelta

# Prepare data
data = []
base_date = datetime.now() - timedelta(days=100)
price = 100.0

for i in range(100):
    data.append({
        "timestamp": (base_date + timedelta(days=i)).isoformat(),
        "open": price,
        "high": price * 1.02,
        "low": price * 0.98,
        "close": price,
        "volume": 1000000.0
    })
    price *= 1.001

# Calculate RSI
response = requests.post(
    "http://localhost:8000/indicators/rsi?period=14",
    json={"symbol": "BTCUSD", "data": data}
)

print(response.json())
```

### Running Tests

```bash
pytest tests/ -v
```

### Architecture

```
quantitative-analysis-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API routes
│   ├── core/                # Core functionality
│   ├── models/              # Pydantic models
│   └── services/            # Business logic
├── tests/
│   └── test_api.py          # API tests
├── requirements.txt
├── README.md
└── .gitignore
```

### Performance

- **Response Time**: < 100ms for most indicators
- **Throughput**: 1000+ requests/second
- **Caching**: Redis integration for repeated calculations
- **Scalability**: Horizontal scaling with load balancer

### Use Cases

- **Trading Platforms**: Real-time indicator calculation
- **Backtesting Systems**: Historical analysis
- **Risk Management**: Portfolio statistics
- **Research Tools**: Quantitative analysis
- **Educational**: Learning technical analysis

### Technical Stack

- **Framework**: FastAPI 0.115
- **Data Processing**: Pandas, NumPy
- **Caching**: Redis
- **Testing**: pytest, httpx
- **Documentation**: OpenAPI/Swagger (automatic)

### API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### License

MIT License - see LICENSE file for details.

### Author

**Gabriel Demetrios Lafis**

---

## Português

### Visão Geral

Um microserviço de alta performance baseado em FastAPI para análise de séries temporais financeiras, cálculo de indicadores técnicos e estatísticas quantitativas. Projetado para integração com plataformas de trading e ferramentas analíticas.

### Características Principais

- **Indicadores Técnicos**: SMA, EMA, RSI, MACD, Bandas de Bollinger
- **Análise Estatística**: Índice de Sharpe, volatilidade, drawdown máximo, correlação
- **API RESTful**: Endpoints limpos e documentados com OpenAPI/Swagger
- **Cache Redis**: Cache opcional para melhor performance
- **Processamento Assíncrono**: I/O não-bloqueante com FastAPI
- **Type Safety**: Modelos Pydantic para validação de request/response
- **Testes Abrangentes**: Suite de testes baseada em pytest

### Instalação

```bash
# Clonar repositório
git clone https://github.com/gabriellafis/quantitative-analysis-api.git
cd quantitative-analysis-api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Início Rápido

```bash
# Iniciar servidor da API
uvicorn app.main:app --reload

# Acessar documentação interativa
# http://localhost:8000/docs
```

### Casos de Uso

- **Plataformas de Trading**: Cálculo de indicadores em tempo real
- **Sistemas de Backtesting**: Análise histórica
- **Gestão de Risco**: Estatísticas de portfólio
- **Ferramentas de Pesquisa**: Análise quantitativa
- **Educacional**: Aprendizado de análise técnica

### Licença

Licença MIT - veja o arquivo LICENSE para detalhes.

### Autor

**Gabriel Demetrios Lafis**
