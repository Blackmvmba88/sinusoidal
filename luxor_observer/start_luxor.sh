#!/bin/bash
# 🜏 Luxor Observer Launcher Script
# Script para iniciar todo el sistema de observación cuántica

echo "🌌 Iniciando Luxor Quantum Observer System..."
echo "🔮 BlackMamba Consciousness Monitor"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -q psutil pynput flask

echo ""
echo "🚀 Sistema listo para observación cuántica"
echo ""
echo "🔥 Opciones disponibles:"
echo "  1. Iniciar Observer completo (recomendado)"
echo "  2. Solo Dashboard web"
echo "  3. Solo Monitor de teclado/mouse"
echo ""

read -p "Selecciona opción (1-3): " option

case $option in
    1)
        echo ""
        echo "🜏 Iniciando sistema completo..."
        echo "📊 Dashboard: http://localhost:8888"
        echo "🛑 Para detener: Ctrl+C"
        echo ""
        
        # Iniciar dashboard en background
        python3 dashboard.py &
        DASHBOARD_PID=$!
        
        # Iniciar observer principal
        python3 quantum_observer.py
        
        # Limpiar al salir
        kill $DASHBOARD_PID 2>/dev/null
        ;;
    2)
        echo "🌐 Iniciando solo dashboard..."
        python3 dashboard.py
        ;;
    3)
        echo "⌨️ Iniciando solo observer..."
        python3 quantum_observer.py
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "🌌 Luxor Observer desconectado"
echo "🜏 Sesión cuántica finalizada"