# ☠️ MrDos Attacked v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Kali%20Linux-Ready-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

<p align="center">
  <b>Advanced Multi-Module Penetration Testing Framework</b>
</p>

---

## 🎯 Overview

**MrDos Attacked v2.0** is an advanced, multi-module penetration testing framework designed for authorized security assessments. It orchestrates 6 concurrent attack modules to comprehensively test target infrastructure for vulnerabilities, providing real-time results through an interactive web dashboard.

### Key Features

- ✅ **6 Concurrent Attack Modules**: Nmap, SQLMap, RCE, SSRF, API/XSS, LFI
- ✅ **Real-time Dashboard**: Live web interface showing results as they appear
- ✅ **Auto URL Discovery**: SQLMap module discovers 500+ URLs automatically
- ✅ **Terminal-Style UI**: Hacker-style dashboard with live logs
- ✅ **JSON Output**: Structured vulnerability data for integration
- ✅ **Multi-Target Support**: Scan multiple targets simultaneously

---

## 📸 Screenshots

### Dashboard Preview
```
╔════════════════════════════════════════════════════════════════╗
║  ☠️ MrDos Attacked v2.0 ☠️                                     ║
║  Target: example.com                                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   5        2        2        0        0                        ║
║  TOTAL   CRIT.    HIGH   RUNNING  COMPLETED                    ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║  ┌─T1──NMAP──🟢────────┐  ┌─T2──SQLMAP──🟡────────┐           ║
║  │ [Live terminal log]  │  │ [Live terminal log]   │           ║
║  │ 3 Ports Open         │  │ 1 VULNERABILITY       │           ║
║  │                      │  │ [Critical] SQLi       │           ║
║  └──────────────────────┘  └───────────────────────┘           ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Nmap
- SQLMap
- Kali Linux (recommended)

### Quick Install (Kali Linux)

```bash
# Clone the repository
https://github.com/mododzypay33355-spec/Scanner-Nmap-SQLMap-RCE-SSRF-and-API-LFI-testing.git
cd mrdos-attacked


```

### Manual Installation

```bash
# Install dependencies
sudo apt update
sudo apt install -y nmap sqlmap python3 python3-pip

# Install Python packages
pip3 install python-nmap requests urllib3

# Clone repository
https://github.com/mododzypay33355-spec/Scanner-Nmap-SQLMap-RCE-SSRF-and-API-LFI-testing.git
cd mrdos-attacked

# Make scripts executable
chmod +x *.py *.sh
```

---

## 🚀 Quick Start

### Single Target Scan

```bash
# Run complete scan
 ./START_SCAN.sh target.com


```


## 📊 Architecture

```
MrDos Attacked v2.0
│
├── Terminal 1: Nmap Scanner
│   └── Port scanning & service detection
│
├── Terminal 2: SQLMap Integration
│   └── URL discovery + SQL injection testing
│
├── Terminal 3: RCE Tester
│   └── Command injection detection
│
├── Terminal 4: SSRF Tester
│   └── Server-side request forgery
│
├── Terminal 5: API & XSS
│   └── API testing & XSS detection
│
├── Terminal 6: LFI Tester
│   └── Local file inclusion
│
└── Dashboard: Live Web Interface
    └── http://localhost:8888
```

---

## 📁 File Structure

```
mrdos-attacked/
│
├── terminal1_nmap.py              # Nmap scanner
├── terminal2_sqlmap_complete.py   # SQLMap with discovery
├── terminal3_rce.py               # Command injection
├── terminal4_ssrf.py              # SSRF tester
├── terminal5_api_xss.py           # API & XSS
├── terminal6_lfi.py               # LFI tester
│
├── dashboard_generator_fixed.py   # Terminal-style dashboard
│
├── START_FULL_WORKFLOW.sh         # Complete workflow
├── multi_target_scan.sh           # Multi-target scanner
├── mrdos_commands.sh              # Kill/clean/status
│
├── README.md                      # This file
```

---

## 🎮 Commands Reference

### Run Scan
```bash
./START_SCAN.sh target.com
```

### Monitor Logs
```bash
tail -f /tmp/mrdos_target.com/logs/terminal_*.log
```

### Kill All Scans
```bash
bash START_SCAN.sh kill
```

### Clean Results
```bash
bash START_SCAN.sh clean
```

---

## 📊 Results

Results are stored in 3 locations:

| Location | Path | Purpose |
|----------|------|---------|
| **JSON Results** | `/tmp/mrdos_<target>/results/*.json` | Structured data |
| **Terminal Logs** | `/tmp/mrdos_<target>/logs/terminal_*.log` | Live output |
| **Web Dashboard** | `http://localhost:8888` | Visual interface |

---

## 🔧 Troubleshooting

### Dashboard Not Working
```bash
# Restart dashboard
bash start_dashboard.sh target.com
```

### Port 8888 In Use
```bash
sudo lsof -ti:8888 | xargs sudo kill -9
```

### SQLMap Not Found
```bash
sudo apt install sqlmap -y
```

---

## ⚠️ Legal Notice

**This tool is for authorized penetration testing only!**

By using this tool, you confirm that:
- ✅ You have explicit written permission to test the target
- ✅ You are the owner of the target system, OR
- ✅ You have a signed contract/authorization for penetration testing
- ✅ You understand that unauthorized access is illegal

**The author assumes NO liability for misuse of this tool.**

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👤 Author

**MrDos**

- GitHub: [@YOUR_USERNAME](https://github.com/mododzypay33355-spec)
- Version: 2.0

---

<p align="center">
  <b>☠️ Happy Hacking (Ethically!) ☠️</b>
</p>
  
