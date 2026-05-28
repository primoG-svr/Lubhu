#!/bin/bash

echo "════════════════════════════════════════════════"
echo "  PAYMENT GATEWAY - QUICK START GUIDE"
echo "════════════════════════════════════════════════"
echo ""

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Sistema detectado: Linux"
    echo ""
    echo "Escolha uma opção:"
    echo "1) Iniciar tudo automaticamente (recomendado)"
    echo "2) Apenas Backend (Docker)"
    echo "3) Apenas Frontend (Next.js)"
    echo "4) Ver instruções manuais"
    echo ""
    read -p "Digite a opção (1-4): " choice
    
    case $choice in
        1)
            echo "Iniciando..."
            bash ./start.sh
            ;;
        2)
            echo "Iniciando Backend..."
            bash ./start.sh --backend-only
            ;;
        3)
            echo "Iniciando Frontend..."
            bash ./start.sh --frontend-only
            ;;
        4)
            cat ./SETUP.md
            ;;
        *)
            echo "Opção inválida"
            ;;
    esac
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Sistema detectado: macOS"
    echo ""
    echo "Escolha uma opção:"
    echo "1) Iniciar tudo automaticamente (recomendado)"
    echo "2) Apenas Backend (Docker)"
    echo "3) Apenas Frontend (Next.js)"
    echo "4) Ver instruções manuais"
    echo ""
    read -p "Digite a opção (1-4): " choice
    
    case $choice in
        1)
            echo "Iniciando..."
            bash ./start.sh
            ;;
        2)
            echo "Iniciando Backend..."
            bash ./start.sh --backend-only
            ;;
        3)
            echo "Iniciando Frontend..."
            bash ./start.sh --frontend-only
            ;;
        4)
            cat ./SETUP.md
            ;;
        *)
            echo "Opção inválida"
            ;;
    esac
else
    echo "💻 Sistema detectado: Windows"
    echo ""
    echo "Clique duplo em: start.bat"
    echo ""
    echo "Ou abra o terminal e execute:"
    echo "  start.bat"
fi