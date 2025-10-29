#!/bin/bash
# 🜏 Luxor Observer Launcher Script - Optimizado y Robusto
# Sistema de observación cuántica BlackMamba

set -e  # Salir en error
set -u  # Error en variables no definidas

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

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "🐍 Python detectado: $PYTHON_VERSION"

# Verificar versión mínima de Python (3.7+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "⚠️  Advertencia: Se recomienda Python 3.7 o superior"
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual optimizado..."
    python3 -m venv venv --prompt "luxor" || {
        echo "❌ Error creando entorno virtual"
        exit 1
    }
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "⚡ Activando entorno cuántico..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ No se encontró el script de activación del venv"
    exit 1
fi

# Verificar e instalar dependencias
echo "📚 Verificando dependencias..."

# Intentar usar requirements.txt si existe
if [ -f "requirements.txt" ]; then
    echo "📄 Usando requirements.txt..."
    max_retries=3
    retry=0
    while [ $retry -lt $max_retries ]; do
        if pip install -q -r requirements.txt; then
            echo "✅ Dependencias instaladas desde requirements.txt"
            break
        else
            retry=$((retry + 1))
            if [ $retry -lt $max_retries ]; then
                echo "⚠️  Reintentando instalación ($retry/$max_retries)..."
                sleep 2
            else
                echo "❌ Error instalando dependencias desde requirements.txt"
                echo "   Intentando instalación manual..."
                break
            fi
        fi
    done
fi

# Verificar cada paquete individualmente
REQUIREMENTS="psutil>=5.9.0 pynput>=1.7.6 flask>=2.3.0"
INSTALL_FAILED=0

for req in $REQUIREMENTS; do
    package_name=${req%%>=*}
    if ! pip show "$package_name" &> /dev/null; then
        echo "📥 Instalando $package_name..."
        
        # Intentar instalación con reintentos
        max_retries=3
        retry=0
        while [ $retry -lt $max_retries ]; do
            if pip install -q "$req"; then
                echo "✅ $package_name instalado correctamente"
                break
            else
                retry=$((retry + 1))
                if [ $retry -lt $max_retries ]; then
                    echo "⚠️  Reintentando instalación de $package_name ($retry/$max_retries)..."
                    sleep 2
                else
                    echo "❌ Error instalando $package_name después de $max_retries intentos"
                    INSTALL_FAILED=1
                fi
            fi
        done
    else
        echo "✅ $package_name ya está instalado"
    fi
done

if [ $INSTALL_FAILED -eq 1 ]; then
    echo ""
    echo "⚠️  Algunas dependencias no se pudieron instalar"
    echo "   Intenta ejecutar: pip install -r requirements.txt"
    echo "   O manualmente: pip install $REQUIREMENTS"
    exit 1
fi

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

# Variables para PIDs
DASHBOARD_PID=""
OBSERVER_PID=""

# Función para manejar señales de forma robusta
cleanup() {
    echo ""
    echo "🛑 Deteniendo procesos..."
    
    # Detener dashboard si está corriendo
    if [ ! -z "$DASHBOARD_PID" ]; then
        if kill -0 $DASHBOARD_PID 2>/dev/null; then
            echo "   Deteniendo dashboard (PID: $DASHBOARD_PID)..."
            kill -TERM $DASHBOARD_PID 2>/dev/null || true
            # Esperar a que termine gracefully
            sleep 1
            # Forzar si aún está corriendo
            if kill -0 $DASHBOARD_PID 2>/dev/null; then
                kill -KILL $DASHBOARD_PID 2>/dev/null || true
            fi
        fi
    fi
    
    # Detener observer si está corriendo
    if [ ! -z "$OBSERVER_PID" ]; then
        if kill -0 $OBSERVER_PID 2>/dev/null; then
            echo "   Deteniendo observer (PID: $OBSERVER_PID)..."
            kill -TERM $OBSERVER_PID 2>/dev/null || true
            sleep 1
            if kill -0 $OBSERVER_PID 2>/dev/null; then
                kill -KILL $OBSERVER_PID 2>/dev/null || true
            fi
        fi
    fi
    
    echo "🌌 Luxor Observer desconectado"
    echo "🜏 Sesión cuántica finalizada"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Validar opción
if ! [[ "$option" =~ ^[1-4]$ ]]; then
    echo "❌ Opción no válida. Usa 1-4."
    exit 1
fi

case $option in
    1)
        echo ""
        echo "🜏 Iniciando sistema cuántico completo..."
        echo "📊 Dashboard: http://localhost:8888"
        echo "📈 Métricas: http://localhost:8888/api/system_metrics"
        echo "❤️  Health: http://localhost:8888/health"
        echo "🛑 Para detener: Ctrl+C"
        echo ""
        
        # Verificar que el puerto 8888 esté disponible
        if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
            echo "⚠️  Puerto 8888 ya está en uso"
            echo "   Usa 'lsof -ti:8888 | xargs kill' para liberar el puerto"
            exit 1
        fi
        
        # Iniciar dashboard en background
        echo "🌐 Iniciando dashboard..."
        python3 dashboard.py > dashboard.log 2>&1 &
        DASHBOARD_PID=$!
        
        # Verificar que el dashboard inició correctamente
        sleep 3
        if ! kill -0 $DASHBOARD_PID 2>/dev/null; then
            echo "❌ Error: Dashboard no pudo iniciarse"
            echo "   Revisa dashboard.log para más detalles"
            exit 1
        fi
        echo "✅ Dashboard iniciado (PID: $DASHBOARD_PID)"
        
        # Iniciar observer principal
        echo "👁️  Iniciando observer cuántico..."
        python3 quantum_observer.py
        ;;
    2)
        echo ""
        echo "🌐 Iniciando dashboard cuántico..."
        echo "📊 Dashboard: http://localhost:8888"
        echo ""
        
        # Verificar puerto
        if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
            echo "⚠️  Puerto 8888 ya está en uso"
            exit 1
        fi
        
        python3 dashboard.py
        ;;
    3)
        echo ""
        echo "👁️  Iniciando observer de consciencia..."
        echo "💾 Datos guardados en: blackmamba_quantum_session.json"
        echo ""
        python3 quantum_observer.py
        ;;
    4)
        echo ""
        echo "🔧 Modo diagnóstico activado"
        echo ""
        echo "📋 Información del sistema:"
        echo "🐍 Python: $(python3 --version)"
        echo "📁 Directorio: $(pwd)"
        echo "💻 Sistema: $(uname -s) $(uname -r)"
        echo ""
        
        echo "📦 Paquetes instalados:"
        if pip list 2>/dev/null | grep -E "(psutil|pynput|flask)" >/dev/null; then
            pip list | grep -E "(psutil|pynput|flask)"
        else
            echo "   ⚠️  No se pudieron listar paquetes"
        fi
        echo ""
        
        echo "🧪 Ejecutando pruebas de importación..."
        python3 -c "
import sys
try:
    import psutil
    print('✅ psutil OK (v{})'.format(psutil.__version__))
except ImportError as e:
    print('❌ psutil NO disponible: {}'.format(e))
    sys.exit(1)

try:
    import pynput
    print('✅ pynput OK')
except ImportError as e:
    print('❌ pynput NO disponible: {}'.format(e))
    sys.exit(1)

try:
    import flask
    print('✅ flask OK (v{})'.format(flask.__version__))
except ImportError as e:
    print('❌ flask NO disponible: {}'.format(e))
    sys.exit(1)

print('\n🎉 Todas las dependencias están disponibles')
" || {
            echo ""
            echo "❌ Error en pruebas de importación"
            echo "   Ejecuta: pip install psutil pynput flask"
            exit 1
        }
        
        echo ""
        echo "🔍 Verificando permisos de accesibilidad..."
        python3 -c "
import subprocess
import sys

# Verificar osascript
try:
    result = subprocess.run(
        ['osascript', '-e', 'tell app \"System Events\" to return name'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print('✅ Permisos de AppleScript OK')
    else:
        print('⚠️  Problema con permisos de AppleScript')
        print('   Puede que necesites dar permisos de accesibilidad')
except FileNotFoundError:
    print('⚠️  osascript no encontrado (no estás en macOS?)')
except subprocess.TimeoutExpired:
    print('⚠️  Timeout en AppleScript')
except Exception as e:
    print(f'❌ Error: {e}')
"
        
        echo ""
        echo "🔌 Verificando puerto 8888..."
        if command -v lsof &> /dev/null; then
            if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo "⚠️  Puerto 8888 está en uso"
                echo "   PIDs usando el puerto:"
                lsof -ti:8888 | xargs -I {} echo "     PID {}"
            else
                echo "✅ Puerto 8888 disponible"
            fi
        else
            echo "⚠️  'lsof' no disponible, no se puede verificar puerto"
        fi
        
        echo ""
        echo "📂 Verificando archivos..."
        if [ -f "quantum_observer.py" ]; then
            echo "✅ quantum_observer.py encontrado"
        else
            echo "❌ quantum_observer.py NO encontrado"
        fi
        
        if [ -f "dashboard.py" ]; then
            echo "✅ dashboard.py encontrado"
        else
            echo "❌ dashboard.py NO encontrado"
        fi
        
        if [ -d "templates" ]; then
            echo "✅ directorio templates/ encontrado"
        else
            echo "❌ directorio templates/ NO encontrado"
        fi
        
        echo ""
        echo "✨ Diagnóstico completado"
        ;;
    *)
        echo "❌ Opción no válida. Usa 1-4."
        exit 1
        ;;
esac