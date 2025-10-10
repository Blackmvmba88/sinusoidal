# 🜏 Luxor Observer Monitoring Guide

This guide shows you how to use the new monitoring tools to observe and debug the Luxor Quantum Observer system.

## Quick Start

### Option 1: All-in-One Monitoring (Recommended for Development)

```bash
cd sinusoidal
./scripts/run_and_monitor.sh
```

This single command:
- ✅ Creates virtual environment if needed
- ✅ Installs dependencies automatically
- ✅ Starts both dashboard and quantum observer
- ✅ Shows live colored logs with error highlighting
- ✅ Cleans up gracefully on Ctrl+C

**What you'll see:**
```
🜏 =================================================
   LUXOR OBSERVER - RUN AND MONITOR
===================================================

✅ Virtual environment activated
🚀 Starting Luxor Observer system...
📂 Log file: /home/user/sinusoidal/logs/luxor_observer.log

🌐 Starting dashboard on port 8888...
👁️  Starting quantum observer...
✅ Both services started successfully!

📊 Dashboard: http://localhost:8888
📊 API State: http://localhost:8888/api/current_state
❤️  Health: http://localhost:8888/health

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Live Log Monitor (colored for errors/warnings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[INFO] 🚀 Iniciando servidor Flask en puerto 8888...
[INFO] 🜏 Luxor Quantum Observer iniciado
[INFO] ⚡ SISTEMA DE OBSERVACIÓN CUÁNTICA ACTIVO ⚡
```

### Option 2: Endpoint Polling (Lightweight Status Check)

In a separate terminal:

```bash
cd sinusoidal
./scripts/poll_monitor.py
```

**What you'll see:**
```
============================================================
🜏 LUXOR OBSERVER POLL MONITOR
============================================================
Monitoring: http://localhost:8888
Interval: 2s
============================================================

🚀 Monitoring started. Press Ctrl+C to stop.

[14:23:45] Current State:
  🧠 Consciousness: ⚡ active_coding
  ⚙️  Workflow: coding
  ⌨️  Keyboard: 5.2/s
  🖱️  Mouse: 1.8/s
  📱 Active App: Code

  Changes detected:
  ~ keyboard_activity: 3.1 → 5.2
  ~ consciousness_level: 💭 contemplative → ⚡ active_coding

[14:23:49] Health Check:
  Status: healthy
  ✅ Data file: True
  ✅ Cache: True

[14:23:55] System Metrics:
  💻 CPU: 23.4%
  🧠 Memory: 67.2%
  🔧 Process: 145.32 MB
```

## Use Cases

### 1. Local Development

**Scenario:** You're developing new features and want immediate feedback on errors.

```bash
# Terminal 1: Run with monitoring
./scripts/run_and_monitor.sh

# Terminal 2: Make code changes
# Terminal 3: Watch the live logs react to your changes
```

**Benefits:**
- Immediate error visibility with red highlighting
- See quantum state transitions in cyan
- Notice warnings in yellow before they become problems

### 2. Debugging Issues

**Scenario:** Something isn't working and you need to trace the problem.

```bash
# Start with full logging
./scripts/run_and_monitor.sh

# Watch for:
# - RED lines (errors) - immediate attention needed
# - YELLOW lines (warnings) - potential issues
# - Missing expected quantum states - logic problems
```

**Common Issues to Look For:**
- `AppleScript timeout` warnings → macOS permissions issue
- `NoSuchProcess` errors → Process tracking problem
- `JSONDecodeError` → Data corruption in session file

### 3. Performance Monitoring

**Scenario:** Check if the observer is running efficiently.

```bash
# Start the poll monitor
./scripts/poll_monitor.py --interval 5

# Watch for:
# - CPU usage trends
# - Memory consumption
# - Response times (should be fast)
# - Event accumulation rates
```

### 4. Integration Testing

**Scenario:** You want to verify the system works end-to-end.

```bash
# Terminal 1: Start system
./scripts/run_and_monitor.sh

# Terminal 2: Monitor state changes
./scripts/poll_monitor.py --interval 1

# Terminal 3: Generate test activity
# - Type rapidly → Watch keyboard_activity spike
# - Move mouse → Watch mouse_activity increase
# - Switch apps → Watch active_apps change
# - Stay idle → Watch consciousness_level become 'contemplative'
```

## Advanced Workflows

### Multi-Terminal Setup

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Terminal 1         │  │  Terminal 2         │  │  Terminal 3         │
│  run_and_monitor.sh │  │  poll_monitor.py    │  │  Web Browser        │
│                     │  │                     │  │  localhost:8888     │
│  Live Logs          │  │  State Changes      │  │  Visual Dashboard   │
│  with Colors        │  │  Real-time          │  │  Graphs & Charts    │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

**Benefits:**
- Logs show implementation details
- Poller shows state changes
- Dashboard shows user-facing view

### Log Analysis

While the system is running, analyze patterns:

```bash
# Count consciousness level changes
grep "consciousness_level" logs/luxor_observer.log | wc -l

# Find all errors
grep -i error logs/luxor_observer.log

# Track active apps over time
grep "active_apps" logs/luxor_observer.log | tail -20

# See quantum state transitions
grep "🜏" logs/luxor_observer.log
```

### Background Operation

Run the system in the background and check it periodically:

```bash
# Start in background (logs to file)
nohup ./scripts/run_and_monitor.sh > /dev/null 2>&1 &

# Check status anytime
./scripts/poll_monitor.py --interval 10

# View logs
tail -f logs/luxor_observer.log

# Stop when done
pkill -f "dashboard.py"
pkill -f "quantum_observer.py"
```

## Troubleshooting with Monitoring Tools

### Problem: Dashboard not responding

```bash
# Check health endpoint
curl http://localhost:8888/health

# If connection refused, check logs
tail -50 logs/luxor_observer.log

# Look for:
# - Port already in use
# - Import errors
# - Permission denied
```

### Problem: Observer not detecting activity

```bash
# Watch for events in poll monitor
./scripts/poll_monitor.py --interval 1

# Generate activity (type, move mouse)
# If keyboard_activity and mouse_activity stay at 0:
# - Check logs for pynput errors
# - Verify accessibility permissions (macOS)
# - Look for "Error in keyboard observer" messages
```

### Problem: High CPU/Memory usage

```bash
# Monitor system metrics
./scripts/poll_monitor.py --interval 2

# Watch:
# - CPU usage (should be < 5% normally)
# - Memory usage (should be < 200MB)
# - Process memory growth over time

# If high, check logs for:
# - Memory leak warnings
# - Excessive event accumulation
# - Runaway threads
```

### Problem: Stale or incorrect data

```bash
# Check data file directly
cat luxor_observer/blackmamba_quantum_session.json | jq .

# Compare with API
curl http://localhost:8888/api/current_state | jq .

# Check cache behavior
curl http://localhost:8888/health | jq .cache_active

# Look for:
# - Last_updated timestamp (should be recent)
# - File write errors in logs
# - Lock contention messages
```

## Comparison with Existing Tools

### start_luxor.sh vs run_and_monitor.sh

| Feature | start_luxor.sh | run_and_monitor.sh |
|---------|----------------|---------------------|
| Interactive menu | ✅ Yes | ❌ No (starts full system) |
| Mode selection | ✅ 4 modes | ❌ Full system only |
| Diagnostic mode | ✅ Yes | ❌ Use separately |
| Live log monitoring | ❌ No | ✅ Yes (colored) |
| Automatic cleanup | ✅ Yes | ✅ Yes |
| Log file creation | ❌ No | ✅ Yes |

**When to use each:**
- `start_luxor.sh` → First-time setup, choosing specific modes, diagnostics
- `run_and_monitor.sh` → Development, debugging, continuous monitoring

## Tips and Best Practices

### 1. Color Coding

Learn to recognize important patterns:
- 🔴 **Red text** → Stop and fix immediately
- 🟡 **Yellow text** → Investigate soon
- 🔵 **Cyan text** → Normal quantum events
- 🟢 **Green text** → Successful operations

### 2. Polling Intervals

Choose based on your needs:
- `--interval 1` → Rapid development (may be noisy)
- `--interval 2` → Default (good balance)
- `--interval 5` → Overview monitoring
- `--interval 10` → Background checking

### 3. Log Management

Keep logs under control:
```bash
# Rotate logs weekly
mv logs/luxor_observer.log logs/luxor_observer.log.$(date +%Y%m%d)

# Clean old logs
find logs/ -name "*.log.*" -mtime +7 -delete

# Compress historical logs
gzip logs/*.log.*
```

### 4. Performance Tuning

If monitoring affects observer performance:
```bash
# Reduce poll frequency
./scripts/poll_monitor.py --interval 5

# Or use curl for one-off checks
curl -s http://localhost:8888/health | jq .

# Check log file size
ls -lh logs/luxor_observer.log
# If > 100MB, rotate it
```

## Examples

### Example 1: Morning Startup

```bash
cd ~/sinusoidal

# Start everything with monitoring
./scripts/run_and_monitor.sh

# In another terminal, verify health
curl http://localhost:8888/health | jq .

# Open dashboard in browser
open http://localhost:8888

# Leave running all day, monitoring in background
```

### Example 2: Bug Investigation

```bash
# Start with full logging
./scripts/run_and_monitor.sh

# Reproduce the bug
# Watch logs for red/yellow lines around the time of the bug

# Take a snapshot of the state
curl http://localhost:8888/api/current_state | jq . > /tmp/bug_state.json

# Save relevant logs
grep -A 5 -B 5 "ERROR" logs/luxor_observer.log > /tmp/bug_logs.txt

# Stop monitoring (Ctrl+C)
# Analyze saved files
```

### Example 3: Performance Test

```bash
# Start poll monitor
./scripts/poll_monitor.py --interval 1 > /tmp/performance_test.txt &
POLL_PID=$!

# Let it run for 5 minutes
sleep 300

# Stop monitoring
kill $POLL_PID

# Analyze results
grep "CPU:" /tmp/performance_test.txt | awk '{sum+=$3; count++} END {print "Avg CPU:", sum/count}'
grep "Memory:" /tmp/performance_test.txt | awk '{sum+=$3; count++} END {print "Avg Memory:", sum/count}'
```

## Next Steps

After mastering these monitoring tools:

1. **Customize** - Edit the scripts to add your own monitoring logic
2. **Extend** - Create new monitoring scripts for specific needs
3. **Integrate** - Add monitoring to your CI/CD pipeline
4. **Share** - Contribute improvements back to the project

See [scripts/README.md](scripts/README.md) for technical details on the monitoring scripts.

---

*Part of the BlackMamba quantum ecosystem - making consciousness observable and debuggable* 🜏
