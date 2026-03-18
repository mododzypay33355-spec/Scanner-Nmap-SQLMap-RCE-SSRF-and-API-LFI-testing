#!/bin/bash
# MrDos Attacked v2.0 - COMPLETE 6-MODULE SCANNER
# Usage: bash START_SCAN.sh <TARGET>

if [ -z "$1" ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║              ☠️  MrDos Attacked v2.0 ☠️                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Usage: bash START_SCAN.sh <target>"
    echo ""
    echo "Examples:"
    echo "  bash START_SCAN.sh mega-technology.info"
    echo "  bash START_SCAN.sh 192.168.1.1"
    echo "  bash START_SCAN.sh target.com"
    echo ""
    exit 1
fi

TARGET="$1"
WORKSPACE="/tmp/mrdos_${TARGET//./_}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ☠️  MrDos Attacked v2.0 ☠️                        ║"
echo "║                   COMPLETE 6-MODULE SCANNER                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Target: $TARGET"
echo "📁 Workspace: $WORKSPACE"
echo ""

# Cleanup
echo "[*] Cleaning up old processes..."
pkill -f "terminal.*py.*$TARGET" 2>/dev/null
kill $(lsof -ti:8888 2>/dev/null) 2>/dev/null
sleep 1

# Create directories
mkdir -p "$WORKSPACE/results" "$WORKSPACE/logs" "$WORKSPACE/web"
cd "$SCRIPT_DIR"

# Launch all 6 terminals
echo "[*] Launching 6 penetration testing modules..."
echo ""

python3 terminal1_nmap.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_1.log" 2>&1 &
echo "  [+] T1 📡 NMAP SCANNER      (PID: $!)"

python3 terminal2_sqlmap.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_2.log" 2>&1 &
echo "  [+] T2 💉 SQLMAP            (PID: $!)"

python3 terminal3_rce.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_3.log" 2>&1 &
echo "  [+] T3 💻 RCE TESTER        (PID: $!)"

python3 terminal4_ssrf.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_4.log" 2>&1 &
echo "  [+] T4 🌐 SSRF TESTER       (PID: $!)"

python3 terminal5_api_xss.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_5.log" 2>&1 &
echo "  [+] T5 🔓 API & XSS          (PID: $!)"

python3 terminal6_lfi.py "$TARGET" "$WORKSPACE" > "$WORKSPACE/logs/terminal_6.log" 2>&1 &
echo "  [+] T6 📁 LFI TESTER        (PID: $!)"

echo ""
sleep 2

# Generate initial dashboard
echo "[*] Generating dashboard..."
python3 dashboard_generator.py "$TARGET" 2>/dev/null

# Start web server
echo "[*] Starting dashboard server on port 8888..."
cd "$WORKSPACE/web"
python3 -m http.server 8888 > /dev/null 2>&1 &
DASH_PID=$!

echo ""
echo "═════════════════════════════════════════════════════════════════"
echo "  ✅ ALL 6 MODULES RUNNING!"
echo "═════════════════════════════════════════════════════════════════"
echo ""
echo "🌐 DASHBOARD: http://localhost:8888"
echo ""
echo "📊 MONITOR COMMANDS:"
echo "   watch -n 2 'ls -lh $WORKSPACE/results/'"
echo "   tail -f $WORKSPACE/logs/terminal_*.log"
echo ""
echo "⏱️  EXPECTED COMPLETION:"
echo "   Nmap:    3-5 min  |  RCE/SSRF: 5-10 min  |  LFI: 5-10 min"
echo "   API/XSS: 10-15 min  |  SQLMap: 10-25 min"
echo ""
echo "🛑 STOP SCAN:"
echo "   pkill -f 'terminal.*py.*$TARGET'"
echo "   kill $DASH_PID"
echo ""
echo "═════════════════════════════════════════════════════════════════"

# Auto-refresh dashboard every 5 seconds
echo "[*] Auto-refreshing dashboard every 5 seconds..."
while true; do
    sleep 5
    python3 "$SCRIPT_DIR/dashboard_generator.py" "$TARGET" > /dev/null 2>&1
done
