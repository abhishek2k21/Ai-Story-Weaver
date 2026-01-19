# AI Story Weaver Pro

*"Weave Living Stories That Adapt, Evolve, and Heal"*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-22+-green.svg)](https://nodejs.org/)

AI Story Weaver Pro is a cutting-edge AI-powered platform that redefines storytelling as an interactive, empathic, and decentralized ecosystem. It generates, adapts, and collaborates on narratives that feel uniquely human, using an advanced agentic architecture.

## Table of Contents

- [AI Story Weaver Pro](#ai-story-weaver-pro)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Technologies Used](#technologies-used)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [DevOps](#devops)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Development Mode](#development-mode)
      - [Using Docker Compose (Recommended)](#using-docker-compose-recommended)
      - [Local Development](#local-development)
    - [Database Setup](#database-setup)
  - [Build and Deployment](#build-and-deployment)
    - [Production Build](#production-build)
    - [CI/CD](#cicd)
  - [Testing](#testing)
    - [Backend Tests](#backend-tests)
    - [Frontend Tests](#frontend-tests)
    - [Integration Tests](#integration-tests)
  - [API Documentation](#api-documentation)
  - [Contributing](#contributing)
    - [Development Guidelines](#development-guidelines)
  - [License](#license)
  - [Recent Updates](#recent-updates)

## Overview

AI Story Weaver Pro leverages an agentic flywheel architecture with five specialized agents:
- **Narrative Causality Engine**: Simulates butterfly effect in stories
- **Emotional Resonance Engine**: Biometric-driven emotional adaptation
- **Collaborative Tension Engine**: Game theory-based multi-user collaboration
- **Cross-Reality Weaving Agent**: Seamless AR/VR integration
- **Ethical Memory Vault**: Blockchain-audited transparency

## Features

- **Agentic Architecture**: Cyclic flywheel for autonomous story evolution
- **Multi-Modal Outputs**: Text, visuals, audio, video, AR/VR experiences
- **Collaborative Tools**: Real-time multi-user sessions with conflict injection
- **Ethical Transparency**: zkEVM blockchain audits and counterfactual bias checks
- **Therapeutic Elements**: Biometric fusion for emotional healing subplots
- **Decentralized Ownership**: NFT minting for story assets

## Project Structure

```
AI-Story-Weaver-Pro/
├── backend/              # Python/FastAPI backend
│   ├── app/              # Main application
│   │   ├── api/          # REST/WebSocket endpoints
│   │   ├── core/         # Configuration and security
│   │   ├── db/           # Database models and connections
│   │   ├── services/     # Agent logic and business logic
│   │   └── main.py       # Application entry point
│   ├── migrations/       # Database schema migrations
│   ├── tests/            # Unit and integration tests
│   └── requirements.txt  # Python dependencies
├── frontend/             # React.js web application
│   ├── src/              # Source code
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom React hooks
│   │   └── utils/        # Utility functions
│   ├── public/           # Static assets
│   └── package.json      # Node.js dependencies
├── shared/               # Cross-platform schemas and types
├── docs/                 # Documentation
│   ├── api-spec.yaml     # OpenAPI specification
│   ├── architecture.md   # System architecture
│   └── whitepaper.md     # Technical whitepaper
├── docker/               # Containerization
│   ├── Dockerfile        # Multi-stage build
│   └── docker-compose.yml # Local development setup
├── kubernetes/           # Production deployment
├── .github/              # CI/CD workflows
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Technologies Used

### Backend
- **Framework**: FastAPI, Uvicorn
- **AI/ML**: LangChain, LangGraph, PyTorch, TensorFlow, Hugging Face Transformers
- **Causality**: DoWhy
- **Game Theory**: NashPy
- **Databases**: PostgreSQL, Pinecone (vectors), Neo4j (graphs), Redis (cache)
- **Blockchain**: Web3.py, Polygon zkEVM
- **Async**: Celery, RabbitMQ
- **Testing**: Pytest

### Frontend
- **Framework**: React.js, React Router
- **State Management**: Redux, Redux Toolkit
- **Real-time**: Socket.io
- **Web3**: Web3.js, Ethers.js
- **3D/AR**: A-Frame, Three.js, WebXR
- **Styling**: CSS Modules (or add preferred styling library)

### DevOps
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Version Control**: Git

## Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 22 or higher with npm
- **Git**: Latest version
- **Docker**: For containerized development (optional but recommended)
- **Docker Compose**: For multi-service setup

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd AI-Story-Weaver-Pro
```

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your actual values:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/storyweaver

   # Security
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here

   # API Keys
   OPENAI_API_KEY=your-openai-key
   ANTHROPIC_API_KEY=your-anthropic-key
   HUGGINGFACE_API_KEY=your-huggingface-key
   ELEVENLABS_API_KEY=your-elevenlabs-key

   # External Services
   REDIS_URL=redis://localhost:6379
   PINECONE_API_KEY=your-pinecone-key
   PINECONE_ENVIRONMENT=your-pinecone-env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=password

   # Blockchain
   WEB3_PROVIDER_URL=https://polygon-rpc.com/
   PRIVATE_KEY=your-private-key

   # App Settings
   ENV=development
   DEBUG=True
   FRONTEND_URL=http://localhost:3000
   ```

## Usage

### Development Mode

#### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access points:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000
- Database: localhost:5432
- Redis: localhost:6379
```

#### Local Development

**Backend**:
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm start
```

### Database Setup

If using Alembic for migrations:
```bash
cd backend
alembic upgrade head
```

## Build and Deployment

### Production Build

1. **Build Docker images**:
   ```bash
   # Backend
   docker build -f docker/Dockerfile -t ai-story-weaver-backend .

   # Frontend
   docker build -f docker/Dockerfile -t ai-story-weaver-frontend --target frontend .
   ```

2. **Deploy to Kubernetes**:
   ```bash
   kubectl apply -f kubernetes/
   ```

### CI/CD

GitHub Actions workflows are configured in `.github/workflows/` for:
- Automated testing
- Code quality checks
- Docker image building
- Deployment to staging/production

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Run with Docker Compose
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Contributing

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and add tests
4. **Commit your changes**:
   ```bash
   git commit -am 'Add some feature'
   ```
5. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure all CI checks pass

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Recent Updates

- ✅ Configured Python virtual environment for backend
- ✅ Installed Python dependencies: FastAPI, LangChain, PyTorch, etc.
- ✅ Set up React frontend with dependencies: React, Redux, Socket.io, Web3.js, etc.
- ✅ Created basic FastAPI app in `backend/app/main.py`
- ✅ Created basic React app in `frontend/src/App.js`
- ✅ Configured multi-stage Dockerfile and Docker Compose
- ✅ Initialized Git repository with proper .gitignore
- ✅ Set up environment variables template
- ✅ Updated README with comprehensive setup and usage instructions
- ✅ Tested backend startup successfully