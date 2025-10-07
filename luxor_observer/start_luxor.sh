#!/bin/bash
# 🜏 Luxor Observer Launcher Script - Optimizado
# Sistema de observación cuántica BlackMamba

set -e  # Salir en error

echo "🜏 " $(printf '=%.0s' {1..50})
echo "    LUXOR QUANTUM OBSERVER SYSTEM"
echo $(printf '=%.0s' {1..54})
echo "🔮 BlackMamba Consciousness Monitor"
echo ""

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3 primero."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual optimizado..."
    python3 -m venv venv --prompt "luxor"
fi

# Activar entorno virtual
echo "⚡ Activando entorno cuántico..."
source venv/bin/activate

# Verificar e instalar dependencias
echo "📚 Verificando dependencias..."
REQUIREMENTS="psutil>=5.9.0 pynput>=1.7.6 flask>=2.3.0"

for req in $REQUIREMENTS; do
    if ! pip show ${req%%>=*} &> /dev/null; then
        echo "📥 Instalando ${req%%>=*}..."
        pip install -q $req
    fi
done

echo ""
echo "🚀 Sistema cuántico listo para observación"
echo ""
echo "🔥 Modos de operación disponibles:"
echo "  1. 🌟 Sistema completo (Observer + Dashboard)"
echo "  2. 🌐 Solo Dashboard web"
echo "  3. 👁️  Solo Observer de consciencia"
echo "  4. 🔧 Modo diagnóstico"
echo ""

read -p "🎯 Selecciona modo (1-4): " option

# Función para manejar señales
cleanup() {
    echo ""
    echo "🛑 Deteniendo procesos..."
    if [ ! -z "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null || true
    fi
    if [ ! -z "$OBSERVER_PID" ]; then
        kill $OBSERVER_PID 2>/dev/null || true
    fi
    echo "🌌 Luxor Observer desconectado"
    echo "🜏 Sesión cuántica finalizada"
    exit 0
}

trap cleanup SIGINT SIGTERM

case $option in
    1)
        echo ""
        echo "🜏 Iniciando sistema cuántico completo..."
        echo "📊 Dashboard: http://localhost:8888"
        echo "� Métricas: http://localhost:8888/api/system_metrics"
        echo "�🛑 Para detener: Ctrl+C"
        echo ""
        
        # Iniciar dashboard en background
        python3 dashboard.py &
        DASHBOARD_PID=$!
        echo "✅ Dashboard iniciado (PID: $DASHBOARD_PID)"
        
        # Esperar un momento para que el dashboard inicie
        sleep 2
        
        # Iniciar observer principal
        echo "✅ Iniciando observer cuántico..."
        python3 quantum_observer.py
        ;;
    2)
        echo "🌐 Iniciando dashboard cuántico..."
        python3 dashboard.py
        ;;
    3)
        echo "👁️ Iniciando observer de consciencia..."
        python3 quantum_observer.py
        ;;
    4)
        echo "🔧 Modo diagnóstico activado"
        echo "🐍 Python: $(python3 --version)"
        echo "📁 Directorio: $(pwd)"
        echo "📦 Paquetes instalados:"
        pip list | grep -E "(psutil|pynput|flask)"
        echo ""
        echo "🧪 Ejecutando pruebas básicas..."
        python3 -c "import psutil, pynput, flask; print('✅ Todas las dependencias OK')"
        echo "🔍 Verificando permisos de accesibilidad..."
        python3 -c "
import subprocess
try:
    result = subprocess.run(['osascript', '-e', 'tell app \"System Events\" to return name'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print('✅ Permisos de AppleScript OK')
    else:
        print('⚠️ Problema con permisos de AppleScript')
except Exception as e:
    print(f'❌ Error: {e}')
"
        ;;
    *)
        echo "❌ Opción no válida. Usa 1-4."
        exit 1
        ;;
esac