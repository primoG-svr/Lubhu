#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   PAYMENT GATEWAY SETUP                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${YELLOW}📍 Diretório raiz: ${SCRIPT_DIR}${NC}"
echo ""

# Function to start backend
start_backend() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔧 INICIANDO BACKEND (Python + MongoDB)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    cd "$SCRIPT_DIR/payment_gateway"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não encontrado. Instale Docker e tente novamente.${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📦 Iniciando serviços Docker...${NC}"
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker iniciado com sucesso!${NC}"
        echo ""
        echo -e "${YELLOW}⏳ Aguardando serviços iniciarem (15s)...${NC}"
        sleep 15
        
        echo -e "${GREEN}✅ Backend rodando em: ${BLUE}http://localhost:8000${NC}"
        echo -e "${GREEN}✅ API Docs em: ${BLUE}http://localhost:8000/docs${NC}"
        echo -e "${GREEN}✅ MongoDB em: ${BLUE}localhost:27017${NC}"
        return 0
    else
        echo -e "${RED}❌ Erro ao iniciar Docker${NC}"
        return 1
    fi
}

# Function to start frontend
start_frontend() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🎨 INICIANDO FRONTEND (Next.js)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    cd "$SCRIPT_DIR/payment_gateway/frontend"
    
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js não encontrado. Instale Node.js 18+ e tente novamente.${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}Node.js version: $(node --version)${NC}"
    echo -e "${YELLOW}npm version: $(npm --version)${NC}"
    echo ""
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📥 Instalando dependências (isso pode levar alguns minutos)...${NC}"
        npm install
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Erro ao instalar dependências${NC}"
            return 1
        fi
        echo -e "${GREEN}✅ Dependências instaladas!${NC}"
    else
        echo -e "${GREEN}✅ Dependências já instaladas${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}🚀 Iniciando servidor Next.js...${NC}"
    npm run dev
}

# Check if running in detached mode (for backend only)
if [ "$1" = "--backend-only" ]; then
    start_backend
    exit $?
fi

if [ "$1" = "--frontend-only" ]; then
    start_frontend
    exit $?
fi

# Start backend in background
start_backend
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Falha ao iniciar backend. Abortando.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ BACKEND INICIADO COM SUCESSO!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}⏳ Aguardando 5 segundos antes de iniciar frontend...${NC}"
sleep 5
echo ""

# Start frontend
start_frontend