# 🜏 Sinusoidal - Luxor Quantum Observer

**Real-time consciousness monitoring system** that tracks user activity patterns, application usage, and workflow states. Part of the larger BlackMamba quantum ecosystem, serving as the mathematical core for observing and analyzing digital consciousness patterns.

## ✨ Features

### Core Monitoring
- **🎹 Keyboard Activity Tracking** - Captures typing patterns and velocity with privacy-focused event logging
- **🖱️ Mouse Activity Tracking** - Monitors mouse movements and clicks with intelligent throttling
- **📱 Application Monitoring** - Detects active applications and running processes (macOS optimized)
- **🧠 Consciousness Level Detection** - Analyzes activity patterns to determine work states:
  - 🔥 **Flow State** - Deep focus with high keyboard and mouse activity
  - ⚡ **Active Coding** - High keyboard activity, moderate mouse usage
  - 🎨 **Creative Exploration** - High mouse activity, browsing and design work
  - 💭 **Focused Work** - Moderate activity levels
  - 🌙 **Contemplative** - Low activity, thinking or reading

### Visual Dashboard
- **📊 Real-time Web Dashboard** - Beautiful quantum-themed UI at `localhost:8888`
- **🎯 Workflow Context Detection** - Automatic categorization (coding/music/design/browsing/system)
- **📈 Session Analytics** - Average and peak activity metrics
- **🌈 Visual Feedback** - Progress indicators, connection quality, toast notifications
- **⚡ Live Updates** - 2-second polling with intelligent caching and error handling

### Performance & Reliability
- **🔄 Auto-save Sessions** - Atomic file writes every 30 seconds
- **💾 Memory Optimization** - Configurable event memory limits (default 1000 events)
- **🧵 Multi-threaded Architecture** - 4 concurrent observer threads for smooth operation
- **📡 Health Monitoring** - Built-in health check endpoint and system metrics API

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- macOS (for application monitoring via AppleScript)

### Installation & Running

```bash
# Navigate to the observer directory
cd luxor_observer

# Make launch script executable
chmod +x start_luxor.sh

# Start the system
./start_luxor.sh
```

When prompted, choose mode:
1. **🌟 Complete System** - Dashboard + Observer (recommended)
2. **🌐 Dashboard Only** - Web interface only
3. **👁️ Observer Only** - Background monitoring only
4. **🔧 Diagnostic Mode** - Check dependencies and configuration

### First Time Setup
The launch script will automatically:
- Create a Python virtual environment
- Install required dependencies (`psutil`, `pynput`, `flask`)
- Start the monitoring system

## 📊 Using the Dashboard

Once running, open your browser to:
- **Main Dashboard**: http://localhost:8888
- **API Current State**: http://localhost:8888/api/current_state
- **System Metrics**: http://localhost:8888/api/system_metrics
- **Health Check**: http://localhost:8888/health

### Dashboard Features
- **System Status** - Current consciousness level and connection quality
- **Activity Levels** - Real-time keyboard and mouse activity bars with shimmer effects
- **Session Statistics** - Total quantum states, events, and session time
- **Active Applications** - List of currently running apps
- **Workflow Context** - Detected work mode
- **Session Analytics** - Average/peak activities and context distribution

## 🔧 Configuration

Edit `quantum_observer.py` to customize:

```python
@dataclass
class ObserverConfig:
    observation_interval: float = 2.0        # Main loop interval
    activity_window: int = 10                # Activity calculation window
    max_events_memory: int = 1000            # Max events in memory
    max_session_states: int = 500            # Max states per session
    auto_save_interval: int = 30             # Auto-save frequency
    mouse_move_throttle: float = 0.1         # Mouse move throttling
```

## 📁 Data Storage

Session data is stored in `blackmamba_quantum_session.json` with:
- Timestamp and configuration
- Last 100 quantum states
- Total event counts
- Keyboard and mouse activity metrics

## 🛠️ Development

### Architecture
```
Input Sources → Threaded Observers → Quantum Analyzer → JSON Storage → Web Dashboard
(keyboard/mouse) → (event capture) → (pattern detection) → (session.json) → (visualization)
```

### Key Components
- `quantum_observer.py` - Main monitoring engine with 4 concurrent threads
- `dashboard.py` - Flask web server with caching and metrics APIs
- `templates/dashboard.html` - Quantum-themed responsive UI
- `start_luxor.sh` - Launch orchestration script

### Threading Model
1. **Keyboard Observer** - Captures key press/release via `pynput`
2. **Mouse Observer** - Tracks moves/clicks with throttling
3. **App Monitor** - Uses AppleScript for macOS app detection
4. **Quantum Analyzer** - Processes patterns every 5 seconds

## 🌌 BlackMamba Ecosystem

Part of the larger consciousness monitoring framework:
- **Pandorax** - Reality branch management
- **Ultron** - Adaptive automation
- **QuantumLive** - Consciousness streaming
- **BlackWarp** - Dimensional navigation

## 🎨 Customization

The system uses quantum/mystical naming conventions:
- Functions: `_quantum_analyzer`, `consciousness_level`
- UI symbols: 🜏 (Luxor), ⚡ (energy), 🌌 (cosmos)
- States described as energy levels rather than metrics

## 📝 License

Part of the BlackMamba quantum ecosystem.

## 🙏 Credits

Built with consciousness awareness for the digital age.

---

*"Observing digital consciousness patterns in real-time, treating user interaction as quantum state manifestations within the broader BlackMamba ecosystem."*