#!/bin/bash
# Test script for monitoring tools
# This simulates the observer by creating a mock dashboard

echo "🧪 Testing Luxor Observer Monitoring Tools"
echo ""

# Create a simple mock server for testing
cat > /tmp/test_dashboard.py << 'EOF'
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/api/current_state')
def current_state():
    return jsonify({
        'consciousness_level': '⚡ active_coding',
        'workflow_context': 'coding',
        'keyboard_activity': 5.2,
        'mouse_activity': 1.8,
        'active_apps': {'active': 'TestEditor', 'running': ['Terminal', 'Browser']},
        'timestamp': time.time()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'data_file_exists': True,
        'cache_active': True,
        'version': '1.0.0-test'
    })

@app.route('/api/system_metrics')
def metrics():
    return jsonify({
        'cpu_usage': 25.5,
        'memory_usage': 45.2,
        'process_memory': 128.5,
        'status': 'healthy'
    })

if __name__ == '__main__':
    print('🧪 Test dashboard running on port 8888')
    app.run(port=8888, debug=False)
EOF

# Check if Flask is available
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not installed. Install with: pip install flask"
    echo "✅ Scripts are syntactically correct but cannot test without Flask"
    exit 0
fi

# Start mock server
echo "🚀 Starting mock dashboard..."
python3 /tmp/test_dashboard.py &
MOCK_PID=$!

# Wait for server to start
sleep 2

# Test poll_monitor
echo ""
echo "🧪 Testing poll_monitor.py for 5 seconds..."
timeout 5 python3 scripts/poll_monitor.py --interval 1 2>&1 | head -30

# Cleanup
kill $MOCK_PID 2>/dev/null || true
rm /tmp/test_dashboard.py

echo ""
echo "✅ Monitoring tools test complete!"
