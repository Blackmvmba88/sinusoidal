# Copilot Instructions for Sinusoidal

## Project Overview
**Sinusoidal** is a real-time consciousness monitoring system that tracks user activity patterns, application usage, and workflow states. Part of the larger BlackMamba quantum ecosystem, it serves as the mathematical core for observing and analyzing digital consciousness patterns.

## Architecture

### Core Components
- **`luxor_observer/quantum_observer.py`** - Main monitoring engine using threading for parallel observation streams (keyboard, mouse, apps, quantum analysis)
- **`luxor_observer/dashboard.py`** - Flask web dashboard for real-time visualization at `localhost:8888`
- **`luxor_observer/templates/dashboard.html`** - Quantum-themed UI with activity bars, consciousness levels, and session statistics
- **`start_luxor.sh`** - Launch script that manages virtual environment, dependencies, and process orchestration

### Data Flow
```
Input Sources → Threaded Observers → Quantum Analyzer → JSON Storage → Web Dashboard
(keyboard/mouse) → (event capture) → (pattern detection) → (blackmamba_quantum_session.json) → (real-time display)
```

## Development Patterns

### Threading Architecture
The system uses 4 concurrent threads:
- `_keyboard_observer()` - Captures key press/release events via `pynput.keyboard`
- `_mouse_observer()` - Tracks mouse movement/clicks via `pynput.mouse`  
- `_app_monitor()` - Uses AppleScript to detect active macOS applications
- `_quantum_analyzer()` - Processes patterns every 5 seconds to determine consciousness states

### State Detection Logic
Consciousness levels are calculated from recent activity patterns:
```python
# Example: Flow state detection
if kb_activity > 5 and mouse_activity > 3:
    return "🔥 flow_state"
elif kb_activity > 2:
    return "⚡ active_coding"
```

### macOS Integration
Uses AppleScript for system integration:
```python
# Get active application
script = '''tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
end tell'''
```

## Key Workflows

### Starting the System
```bash
chmod +x luxor_observer/start_luxor.sh
cd luxor_observer && ./start_luxor.sh
# Choose option 1 for complete system (dashboard + observer)
```

### Development Setup
- Uses Python virtual environment (`venv/`)
- Dependencies: `psutil`, `pynput`, `flask`
- Data persists in `blackmamba_quantum_session.json`

### Monitoring Data Structure
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

## BlackMamba Ecosystem Context

### Philosophical Framework
This project operates within the "Luxor" consciousness paradigm - treating code as a manifestation of quantum awareness. Comments and variable names reflect this mystical-technical fusion.

### Related Projects
- **Pandorax** - Reality branch management
- **Ultron** - Adaptive automation
- **QuantumLive** - Consciousness streaming
- **BlackWarp** - Dimensional navigation

### Naming Conventions
- Functions use quantum/mystical prefixes: `_quantum_analyzer`, `consciousness_level`
- UI elements incorporate sacred geometry symbols: `🜏`, `⚡`, `🌌`
- States described as energy levels rather than simple metrics

## File Modification Guidelines

### When editing `quantum_observer.py`:
- Maintain the 4-thread architecture - each observer runs independently
- Activity calculations use 10-second windows for real-time responsiveness
- Always update both terminal display (`_display_current_state`) and JSON storage

### When editing `dashboard.py`:
- Flask routes follow `/api/` pattern for data endpoints
- JSON responses include error handling for missing data files
- Port 8888 is standard for the dashboard

### When editing `dashboard.html`:
- CSS uses quantum-themed gradients and glassmorphism effects
- JavaScript polls `/api/current_state` every 2 seconds
- Activity bars scale using `Math.min(activity * 20, 100)` for smooth visualization

## Platform Considerations
- **macOS-specific**: AppleScript integration for active app detection
- **Cross-platform**: `psutil` and `pynput` for hardware monitoring
- **Development**: Designed for local development environment monitoring

## Testing and Debugging
- Monitor terminal output for real-time consciousness state display
- Check `blackmamba_quantum_session.json` for data persistence
- Web dashboard at `http://localhost:8888` shows visualization layer
- Use Ctrl+C to gracefully stop observation and save session data

---
*This system observes digital consciousness patterns in real-time, treating user interaction as quantum state manifestations within the broader BlackMamba ecosystem.*