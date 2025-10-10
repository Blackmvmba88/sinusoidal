#!/bin/bash
# 🜏 Luxor Observer Run and Monitor Script
# Starts the Luxor Observer system and monitors logs in real-time

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LUXOR_DIR="$PROJECT_ROOT/luxor_observer"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/luxor_observer.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Create logs directory
mkdir -p "$LOG_DIR"

echo -e "${CYAN}🜏 =================================================${NC}"
echo -e "${CYAN}   LUXOR OBSERVER - RUN AND MONITOR${NC}"
echo -e "${CYAN}===================================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping Luxor Observer...${NC}"
    
    # Kill observer and dashboard processes
    pkill -f "quantum_observer.py" 2>/dev/null || true
    pkill -f "dashboard.py" 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if venv exists in luxor_observer directory
if [ ! -d "$LUXOR_DIR/venv" ]; then
    echo -e "${YELLOW}📦 Virtual environment not found. Creating...${NC}"
    cd "$LUXOR_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q psutil pynput flask
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    cd "$LUXOR_DIR"
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
fi

echo ""
echo -e "${BLUE}🚀 Starting Luxor Observer system...${NC}"
echo -e "${CYAN}📂 Log file: $LOG_FILE${NC}"
echo ""

# Start dashboard in background
echo -e "${CYAN}🌐 Starting dashboard on port 8888...${NC}"
python3 dashboard.py > "$LOG_FILE" 2>&1 &
DASHBOARD_PID=$!

sleep 2

# Start quantum observer in background
echo -e "${CYAN}👁️  Starting quantum observer...${NC}"
python3 quantum_observer.py >> "$LOG_FILE" 2>&1 &
OBSERVER_PID=$!

sleep 2

# Check if processes are running
if kill -0 $DASHBOARD_PID 2>/dev/null && kill -0 $OBSERVER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Both services started successfully!${NC}"
    echo ""
    echo -e "${CYAN}📊 Dashboard: ${GREEN}http://localhost:8888${NC}"
    echo -e "${CYAN}📊 API State: ${GREEN}http://localhost:8888/api/current_state${NC}"
    echo -e "${CYAN}❤️  Health: ${GREEN}http://localhost:8888/health${NC}"
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}📝 Live Log Monitor (colored for errors/warnings)${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Tail the log file with color highlighting
    tail -f "$LOG_FILE" | while read -r line; do
        if [[ "$line" =~ ERROR|error|Error ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ "$line" =~ WARNING|warning|Warning ]]; then
            echo -e "${YELLOW}$line${NC}"
        elif [[ "$line" =~ quantum|consciousness|🜏|⚡|🔥 ]]; then
            echo -e "${CYAN}$line${NC}"
        elif [[ "$line" =~ INFO|Starting|Iniciando ]]; then
            echo -e "${GREEN}$line${NC}"
        else
            echo "$line"
        fi
    done
else
    echo -e "${RED}❌ Failed to start services. Check logs:${NC}"
    echo -e "${YELLOW}$LOG_FILE${NC}"
    cat "$LOG_FILE"
    exit 1
fi
