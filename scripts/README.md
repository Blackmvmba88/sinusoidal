# 🜏 Luxor Observer Monitoring Scripts

This directory contains monitoring utilities to help you observe and debug the Luxor Quantum Observer system.

## Scripts

### 1. run_and_monitor.sh

**Purpose:** Starts the Luxor Observer system (both dashboard and quantum observer) and monitors logs in real-time with colored output.

**Features:**
- Automatically creates and activates virtual environment
- Starts both dashboard (port 8888) and quantum observer
- Redirects all output to logs/luxor_observer.log
- Displays live log tail with color highlighting:
  - 🔴 Red: Errors
  - 🟡 Yellow: Warnings
  - 🔵 Cyan: Quantum/consciousness events
  - 🟢 Green: Info messages
- Graceful cleanup on Ctrl+C

**Usage:**
```bash
# Make executable (first time only)
chmod +x scripts/run_and_monitor.sh

# Run the monitor
./scripts/run_and_monitor.sh

# Or from the scripts directory
cd scripts
./run_and_monitor.sh
```

**What it does:**
1. Checks for virtual environment (creates if needed)
2. Installs dependencies if needed (psutil, pynput, flask)
3. Starts dashboard.py in background
4. Starts quantum_observer.py in background
5. Tails the log file with colored output
6. Cleans up processes on exit (Ctrl+C)

### 2. poll_monitor.py

**Purpose:** Polls the Luxor Observer dashboard endpoints and displays changes in real-time without needing to check logs or the web interface.

**Features:**
- Monitors `/api/current_state` endpoint continuously
- Displays consciousness level, workflow context, and activity metrics
- Shows active applications
- Detects and highlights changes between polls
- Periodically checks `/health` and `/api/system_metrics`
- Works with either `requests` library or built-in `urllib`
- Colored terminal output for easy reading

**Usage:**
```bash
# Make executable (first time only)
chmod +x scripts/poll_monitor.py

# Run with defaults (localhost:8888, 2 second interval)
./scripts/poll_monitor.py

# Specify custom URL
./scripts/poll_monitor.py --url http://localhost:8888

# Change polling interval to 5 seconds
./scripts/poll_monitor.py --interval 5

# Get help
./scripts/poll_monitor.py --help
```

**Requirements:**
- Python 3.6+
- Optional: `requests` library (falls back to urllib if not available)

**Output Example:**
```
🜏 LUXOR OBSERVER POLL MONITOR
==================================================
Monitoring: http://localhost:8888
Interval: 2s
==================================================

[14:23:45] Current State:
  🧠 Consciousness: ⚡ active_coding
  ⚙️  Workflow: coding
  ⌨️  Keyboard: 5.2/s
  🖱️  Mouse: 1.8/s
  📱 Active App: Code

  Changes detected:
  ~ keyboard_activity: 3.1 → 5.2
  ~ consciousness_level: 💭 contemplative → ⚡ active_coding
```

## Typical Workflows

### Development Workflow

1. **Start the system with monitoring:**
   ```bash
   ./scripts/run_and_monitor.sh
   ```
   This gives you live logs with colored output to catch errors immediately.

2. **In another terminal, use the poller for quick status checks:**
   ```bash
   ./scripts/poll_monitor.py
   ```
   This shows you what's happening without opening the web dashboard.

### Debugging Workflow

1. **Start with the shell monitor to see all logs:**
   ```bash
   ./scripts/run_and_monitor.sh
   ```

2. **If you see errors, check the full log file:**
   ```bash
   tail -f logs/luxor_observer.log
   # or
   less logs/luxor_observer.log
   ```

3. **To check specific endpoints:**
   ```bash
   # Check health
   curl http://localhost:8888/health | jq
   
   # Check current state
   curl http://localhost:8888/api/current_state | jq
   
   # Check system metrics
   curl http://localhost:8888/api/system_metrics | jq
   ```

### Testing Workflow

1. **Start the system:**
   ```bash
   ./scripts/run_and_monitor.sh
   ```

2. **In another terminal, monitor changes:**
   ```bash
   ./scripts/poll_monitor.py
   ```

3. **Generate activity** (type, move mouse, switch apps) and watch the monitors react

4. **Verify in web dashboard:**
   Open http://localhost:8888 in your browser

## Troubleshooting

### run_and_monitor.sh issues

**Problem:** Script fails with "command not found"
```bash
# Solution: Make it executable
chmod +x scripts/run_and_monitor.sh
```

**Problem:** "Python 3 not found"
```bash
# Solution: Install Python 3
# macOS: brew install python3
# Linux: sudo apt-get install python3
```

**Problem:** Services won't start
```bash
# Solution: Check the log file for errors
cat logs/luxor_observer.log

# Or run manually to see errors
cd luxor_observer
source venv/bin/activate
python3 dashboard.py
```

### poll_monitor.py issues

**Problem:** "Connection refused"
```bash
# Solution: Make sure the dashboard is running
# Check with:
curl http://localhost:8888/health

# Or start it with:
./scripts/run_and_monitor.sh
```

**Problem:** "Module not found: requests"
```bash
# Solution: The script will use urllib as fallback
# Or install requests:
pip install requests
```

## Log Files

All logs are stored in the `logs/` directory (automatically created):
- `logs/luxor_observer.log` - Combined output from dashboard and observer

The logs directory is ignored by git (see .gitignore).

## Integration with Existing Tools

These scripts complement the existing `luxor_observer/start_luxor.sh`:
- Use `start_luxor.sh` for interactive mode selection (dashboard only, observer only, etc.)
- Use `run_and_monitor.sh` for development with live log monitoring
- Use `poll_monitor.py` for quick status checks without opening the web interface

## Advanced Usage

### Running in Background

```bash
# Start with nohup (logs to file)
nohup ./scripts/run_and_monitor.sh > /dev/null 2>&1 &

# Check processes
ps aux | grep -E "dashboard|quantum_observer"

# Stop processes
pkill -f "dashboard.py"
pkill -f "quantum_observer.py"
```

### Custom Log Analysis

```bash
# Filter for errors only
tail -f logs/luxor_observer.log | grep -i error

# Count events by type
grep "consciousness_level" logs/luxor_observer.log | wc -l

# Extract quantum states
grep "🧠" logs/luxor_observer.log | tail -20
```

### Monitoring Multiple Intervals

```bash
# Terminal 1: Live logs
./scripts/run_and_monitor.sh

# Terminal 2: Fast polling (every 1 second)
./scripts/poll_monitor.py --interval 1

# Terminal 3: Slow polling (every 10 seconds) for overview
./scripts/poll_monitor.py --interval 10
```

## Contributing

When adding new monitoring scripts:
1. Add them to this directory
2. Make them executable (`chmod +x`)
3. Document them in this README
4. Follow the quantum/consciousness naming conventions
5. Use colored output for better readability

---

*Part of the BlackMamba quantum ecosystem - observing consciousness patterns in real-time* 🜏
