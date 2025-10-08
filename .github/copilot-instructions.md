# Instrucciones de Copilot para Sinusoidal

## Descripción General del Proyecto
**Sinusoidal** es un sistema de monitoreo de consciencia en tiempo real que rastrea patrones de actividad del usuario, uso de aplicaciones y estados de flujo de trabajo. Como parte del ecosistema cuántico BlackMamba más amplio, sirve como el núcleo matemático para observar y analizar patrones de consciencia digital.

## Arquitectura

### Componentes Principales
- **`luxor_observer/quantum_observer.py`** - Motor de monitoreo principal usando threading para flujos de observación paralelos (teclado, mouse, apps, análisis cuántico)
- **`luxor_observer/dashboard.py`** - Dashboard web Flask para visualización en tiempo real en `localhost:8888`
- **`luxor_observer/templates/dashboard.html`** - UI con tema cuántico con barras de actividad, niveles de consciencia y estadísticas de sesión
- **`start_luxor.sh`** - Script de inicio que gestiona el entorno virtual, dependencias y orquestación de procesos

### Flujo de Datos
```
Input Sources → Threaded Observers → Quantum Analyzer → JSON Storage → Web Dashboard
(keyboard/mouse) → (event capture) → (pattern detection) → (blackmamba_quantum_session.json) → (real-time display)
```

## Patrones de Desarrollo

### Arquitectura de Threading
El sistema usa 4 hilos concurrentes:
- `_keyboard_observer()` - Captura eventos de presión/liberación de teclas vía `pynput.keyboard`
- `_mouse_observer()` - Rastrea movimientos/clics del mouse vía `pynput.mouse`  
- `_app_monitor()` - Usa AppleScript para detectar aplicaciones activas en macOS
- `_quantum_analyzer()` - Procesa patrones cada 5 segundos para determinar estados de consciencia

### Lógica de Detección de Estados
Los niveles de consciencia se calculan a partir de patrones de actividad recientes:
```python
# Example: Flow state detection
if kb_activity > 5 and mouse_activity > 3:
    return "🔥 flow_state"
elif kb_activity > 2:
    return "⚡ active_coding"
```

### Integración con macOS
Usa AppleScript para integración con el sistema:
```python
# Get active application
script = '''tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
end tell'''
```

## Flujos de Trabajo Clave

### Iniciar el Sistema
```bash
chmod +x luxor_observer/start_luxor.sh
cd luxor_observer && ./start_luxor.sh
# Choose option 1 for complete system (dashboard + observer)
```

### Configuración de Desarrollo
- Usa entorno virtual de Python (`venv/`)
- Dependencias: `psutil`, `pynput`, `flask`
- Los datos persisten en `blackmamba_quantum_session.json`

### Estructura de Datos de Monitoreo
```python
@dataclass
class QuantumState:
    timestamp: str
    active_apps: List[str]
    keyboard_activity: float  # events per second
    mouse_activity: float
    workflow_context: str     # coding/music/design/browsing/system
    consciousness_level: str  # flow_state/active_coding/creative_exploration/contemplative
```

## Contexto del Ecosistema BlackMamba

### Marco Filosófico
Este proyecto opera dentro del paradigma de consciencia "Luxor" - tratando el código como una manifestación de la consciencia cuántica. Los comentarios y nombres de variables reflejan esta fusión místico-técnica.

### Proyectos Relacionados
- **Pandorax** - Gestión de ramas de realidad
- **Ultron** - Automatización adaptativa
- **QuantumLive** - Streaming de consciencia
- **BlackWarp** - Navegación dimensional

### Convenciones de Nomenclatura
- Las funciones usan prefijos cuánticos/místicos: `_quantum_analyzer`, `consciousness_level`
- Los elementos de UI incorporan símbolos de geometría sagrada: `🜏`, `⚡`, `🌌`
- Los estados se describen como niveles de energía en lugar de métricas simples

## Guías para Modificación de Archivos

### Al editar `quantum_observer.py`:
- Mantén la arquitectura de 4 hilos - cada observador se ejecuta independientemente
- Los cálculos de actividad usan ventanas de 10 segundos para responsividad en tiempo real
- Siempre actualiza tanto la visualización en terminal (`_display_current_state`) como el almacenamiento JSON

### Al editar `dashboard.py`:
- Las rutas Flask siguen el patrón `/api/` para endpoints de datos
- Las respuestas JSON incluyen manejo de errores para archivos de datos faltantes
- El puerto 8888 es el estándar para el dashboard

### Al editar `dashboard.html`:
- El CSS usa gradientes con tema cuántico y efectos de glassmorphism
- JavaScript consulta `/api/current_state` cada 2 segundos
- Las barras de actividad escalan usando `Math.min(activity * 20, 100)` para visualización suave

## Consideraciones de Plataforma
- **Específico de macOS**: Integración AppleScript para detección de app activa
- **Multi-plataforma**: `psutil` y `pynput` para monitoreo de hardware
- **Desarrollo**: Diseñado para monitoreo de entorno de desarrollo local

## Pruebas y Depuración
- Monitorea la salida del terminal para visualización de estado de consciencia en tiempo real
- Revisa `blackmamba_quantum_session.json` para persistencia de datos
- Dashboard web en `http://localhost:8888` muestra la capa de visualización
- Usa Ctrl+C para detener la observación de forma elegante y guardar datos de sesión

## Vocabulario Técnico Clave
- **Consciousness Level** (Nivel de Consciencia): Estado detectado de enfoque y actividad
- **Flow State** (Estado de Flujo): Nivel máximo de concentración y productividad
- **Quantum Observer** (Observador Cuántico): Sistema de monitoreo en tiempo real
- **Threading**: Ejecución paralela de múltiples observadores simultáneos
- **Workflow Context** (Contexto de Flujo de Trabajo): Tipo de actividad detectada (código, música, diseño, etc.)

---
*Este sistema observa patrones de consciencia digital en tiempo real, tratando la interacción del usuario como manifestaciones de estado cuántico dentro del ecosistema BlackMamba más amplio.*