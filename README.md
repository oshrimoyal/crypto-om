# Crypto‑OM Trading System

This repository contains a modular cryptocurrency trading platform built from the ground up to implement the strategies described in the accompanying research.  The system uses an event‑driven architecture with dedicated services for data ingestion, signal generation, risk/portfolio management, execution, API access and orchestration.

## Directory Structure

```
crypto-om/
├── services/               # Micro‑services and supporting modules
│   ├── data/              # Market and on‑chain data adapters
│   ├── signals/           # Strategy engines
│   ├── risk/              # Risk and portfolio management
│   ├── execution/         # Order routing and exchange adapters
│   ├── api/               # FastAPI server exposing REST endpoints
│   ├── workers/           # Background jobs and schedulers
│   ├── utils/             # Shared utilities (config, logging, messaging)
│   └── backtester/        # Event‑driven backtester (work in progress)
├── configs/               # YAML configuration files
├── dashboards/            # Grafana dashboard JSON definitions
├── scripts/               # Utility scripts (e.g. database migrations)
├── tests/                 # Unit and integration tests
├── api/openapi.yaml       # OpenAPI v3 specification
├── docker-compose.yml     # Compose definition for local development
├── Dockerfile             # Base image used by service containers
├── .env.example           # Environment variable template
└── .github/workflows/ci.yml # CI pipeline definition
```

See the design document for a full description of system components and architecture.

## Quick Start (Local)

1. Copy the example environment file and fill in your exchange API keys and secrets:

   ```bash
   cp .env.example .env
   ```

2. Start the entire stack using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Visit `http://localhost:8000/docs` for interactive API documentation and `http://localhost:3000` to access Grafana dashboards.

## Testing

The `tests/` directory contains unit tests for core modules.  Run them with pytest:

```bash
docker-compose run --rm api pytest -q
```

## License

This project is provided for educational and research purposes and carries no warranty.  Use at your own risk.