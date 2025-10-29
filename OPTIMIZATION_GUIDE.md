# Testing and Validation Guide

This document describes the optimizations and robustness improvements made to Sinusoidal (Luxor Quantum Observer) and how to validate them.

## Changes Summary

### 1. Critical Bug Fixes

#### quantum_observer.py
- **Fixed**: Removed unreachable code in `_save_session_data()` method
  - **Before**: Duplicate cleanup code after `raise` statement (never executed)
  - **After**: Single, proper cleanup with OSError handling
  - **Impact**: Eliminates dead code and improves cleanup reliability

### 2. Error Handling Improvements

#### quantum_observer.py
- **`_save_session_data()`**: Added OSError handling for temporary file cleanup
- **`stop_observation()`**: 
  - Added check to prevent double-stop
  - Increased thread join timeout from 1s to 2s
  - Added thread index logging for better debugging
  - Specific RuntimeError handling
  
- **`_app_monitor()`**:
  - Fixed time calculation: Uses `.total_seconds()` for accurate elapsed time
  - Added consecutive error counter with automatic pause after 10 errors
  - Better subprocess error handling (FileNotFoundError, OSError)
  - Improved AppleScript error recovery
  - Added `ad_value=""` parameter to psutil.process_iter for robustness

- **`_calculate_keyboard_activity()` & `_calculate_mouse_activity()`**:
  - Added type validation for dictionary entries
  - Added exception handling with logging
  - Ensures non-negative return values

- **`_detect_workflow_context()`**:
  - Added exception handling
  - Added validation for empty active app
  - Expanded application mapping (PyCharm, IntelliJ, Atom, Vim, etc.)

- **`_detect_consciousness_level()`**:
  - Added input validation and type casting
  - ValueError and TypeError handling

#### dashboard.py
- **`get_current_state()`**:
  - Granular error handling (OSError, IOError, JSONDecodeError)
  - Better file validation
  - Timestamps on all error responses
  - Fallback to basic data if enrichment fails
  - Detailed error logging with `exc_info=True`

- **`_enhance_data()`**:
  - Type validation for states list
  - Filter for valid state dictionaries
  - Try-catch for numeric conversions
  - Use of `collections.Counter` for efficiency
  - Fallback to original data on errors

- **`get_system_metrics()`**:
  - Specific psutil exception handling
  - Added process CPU metric
  - Individual try-catch for memory and process metrics
  - Graceful degradation (return 0 on errors)

### 3. Script Improvements

#### start_luxor.sh
- **Safety**: Added `set -u` for undefined variable detection
- **Python validation**: Check for Python 3.7+ minimum version
- **Dependency management**:
  - Support for requirements.txt with fallback
  - 3-retry mechanism for each package
  - Better error messages
  
- **Process management**:
  - Robust cleanup with TERM → KILL progression
  - Process existence verification before kill
  - Sleep between signals for graceful shutdown
  - Dashboard logging to file (dashboard.log)
  
- **Port checking**: Verify port 8888 availability before starting
- **Process validation**: Verify dashboard started successfully
- **Input validation**: Reject invalid mode selections
- **Enhanced diagnostics**:
  - Individual package version checks
  - Import tests per package
  - AppleScript permission verification
  - Port availability check
  - File existence verification

### 4. New Features

- **requirements.txt**: Standard Python dependency file for easier installation
- **Dashboard logging**: Output captured to dashboard.log for debugging

## How to Test

### 1. Syntax Validation

```bash
# Python files
cd luxor_observer
python3 -m py_compile quantum_observer.py dashboard.py

# Shell script
bash -n start_luxor.sh
```

### 2. Dependency Installation

```bash
cd luxor_observer

# Test with requirements.txt
pip install -r requirements.txt

# Verify installations
pip show psutil pynput flask
```

### 3. Diagnostic Mode

```bash
cd luxor_observer
./start_luxor.sh
# Choose option 4 (Diagnostic mode)
```

Expected output should show:
- ✅ All dependencies OK
- ✅ Python 3.7+ detected
- ✅ Port 8888 available
- ✅ All files found
- ✅ AppleScript permissions (macOS only)

### 4. Observer Testing

```bash
cd luxor_observer
./start_luxor.sh
# Choose option 3 (Observer only)
# Press Ctrl+C after a few seconds
```

Verify:
- No Python exceptions
- Session data saved to `blackmamba_quantum_session.json`
- Clean shutdown with "Sesión cuántica finalizada" message

### 5. Dashboard Testing

```bash
cd luxor_observer
./start_luxor.sh
# Choose option 2 (Dashboard only)
# In another terminal, test endpoints:
curl http://localhost:8888/health
curl http://localhost:8888/api/system_metrics
curl http://localhost:8888/api/current_state
```

Verify:
- All endpoints return JSON
- No 500 errors
- Health endpoint shows "healthy" status
- Proper error messages when observer not running

### 6. Complete System Testing

```bash
cd luxor_observer
./start_luxor.sh
# Choose option 1 (Complete system)
# Open browser to http://localhost:8888
# Verify dashboard displays data
# Type and move mouse to generate activity
# Press Ctrl+C to stop
```

Verify:
- Dashboard shows real-time updates
- Activity bars change with keyboard/mouse usage
- Clean shutdown of both processes
- Data saved to JSON file

### 7. Error Recovery Testing

#### Test port conflict:
```bash
# Terminal 1
cd luxor_observer
./start_luxor.sh
# Choose option 2

# Terminal 2
cd luxor_observer
./start_luxor.sh
# Choose option 2
# Should see: "⚠️ Puerto 8888 ya está en uso"
```

#### Test missing dependencies:
```bash
cd luxor_observer
# Temporarily rename requirements.txt
mv requirements.txt requirements.txt.bak
# Uninstall a package
pip uninstall -y psutil
# Try to run
./start_luxor.sh
# Should auto-install psutil
# Restore requirements.txt
mv requirements.txt.bak requirements.txt
```

#### Test corrupted data file:
```bash
# Create invalid JSON
echo "invalid json" > blackmamba_quantum_session.json
# Start dashboard
./start_luxor.sh
# Choose option 2
# In another terminal:
curl http://localhost:8888/api/current_state
# Should return proper error JSON, not crash
```

## Performance Improvements

1. **Caching**: Dashboard uses 2-second cache for state data
2. **Counter usage**: `_enhance_data` uses Counter for O(n) context analysis
3. **Throttling**: Mouse events throttled to 0.25s to reduce overhead
4. **Deque limits**: Fixed-size deques prevent memory growth
5. **AppleScript caching**: 2-second cache for app detection

## Security Improvements

1. **File operations**: Atomic writes with temp file + os.replace
2. **Input validation**: All numeric inputs validated and bounded
3. **Error messages**: No sensitive data leaked in error responses
4. **Process isolation**: Each component can run independently

## Compatibility

- **Python**: 3.7+ (3.9+ recommended)
- **OS**: macOS (for AppleScript), Linux partial support
- **Dependencies**: See requirements.txt

## Known Limitations

1. **AppleScript**: macOS-specific, will fail gracefully on other OS
2. **Accessibility**: pynput may require accessibility permissions
3. **Port 8888**: Hardcoded, conflicts if already in use
4. **Process monitoring**: psutil may not capture all processes

## Troubleshooting

### Dashboard won't start
```bash
# Check logs
cat luxor_observer/dashboard.log

# Verify port
lsof -i :8888
```

### Observer missing events
```bash
# macOS: Grant accessibility permissions
System Preferences → Security & Privacy → Privacy → Accessibility
# Add Terminal or your terminal app
```

### High CPU usage
- Reduce `observation_interval` in ObserverConfig
- Increase `mouse_move_throttle`

### Memory growing
- Reduce `max_events_memory` and `max_session_states` in ObserverConfig

## Validation Checklist

- [ ] All Python files compile without errors
- [ ] Shell script passes bash -n syntax check
- [ ] Diagnostic mode shows all green checkmarks
- [ ] Observer starts and stops cleanly
- [ ] Dashboard serves all endpoints successfully
- [ ] Complete system shows real-time updates
- [ ] Port conflict detection works
- [ ] Dependency auto-installation works
- [ ] Error recovery doesn't crash processes
- [ ] Session data saves correctly
- [ ] Cleanup function terminates processes
- [ ] Log files are created and populated

## Conclusion

The system is now significantly more robust with:
- **No critical bugs**: All unreachable code removed
- **Better error handling**: Specific exceptions caught and handled
- **Improved logging**: More informative debug messages
- **Safer operations**: Input validation and atomic file writes
- **Better recovery**: Automatic retries and fallbacks
- **Enhanced diagnostics**: Comprehensive testing mode

The system can now handle edge cases, recovers from errors gracefully, and provides better feedback to users.
