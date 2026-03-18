#!/usr/bin/env python3
"""Dashboard Generator - Creates live dashboard from scan results"""
import os, json, glob
from datetime import datetime

def read_results(workspace):
    """Read all 6 terminal results"""
    results = {}
    files = {
        't1': 'nmap_scan.json', 't2': 'sqlmap_scan.json', 't3': 'rce_scan.json',
        't4': 'ssrf_scan.json', 't5': 'api_xss_scan.json', 't6': 'lfi_scan.json'
    }
    
    for term_id, filename in files.items():
        filepath = os.path.join(workspace, 'results', filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Read log preview
                log_file = os.path.join(workspace, 'logs', f'terminal_{term_id[1]}.log')
                if os.path.exists(log_file):
                    with open(log_file, 'r') as lf:
                        lines = lf.readlines()
                        data['log_preview'] = ''.join(lines[-15:])
                else:
                    data['log_preview'] = 'Scanning...'
                
                results[term_id] = data
            except Exception as e:
                results[term_id] = {'status': 'error', 'error': str(e), 'vulnerabilities': [], 'log_preview': f'Error: {e}'}
        else:
            results[term_id] = {'status': 'waiting', 'vulnerabilities': [], 'log_preview': 'Waiting...', 'target': 'unknown'}
    
    return results

def generate_dashboard(workspace, target):
    """Generate complete dashboard HTML"""
    results = read_results(workspace)
    
    # Calculate totals
    total_vulns = sum(len(r.get('vulnerabilities', [])) for r in results.values())
    critical = sum(1 for r in results.values() for v in r.get('vulnerabilities', []) if v.get('severity') == 'Critical')
    high = sum(1 for r in results.values() for v in r.get('vulnerabilities', []) if v.get('severity') == 'High')
    running = sum(1 for r in results.values() if r.get('status') == 'running')
    completed = sum(1 for r in results.values() if r.get('status') == 'completed')
    
    # Build terminal cards
    terminal_info = {
        't1': {'name': 'NMAP SCANNER', 'icon': '📡', 'color': '#00ff00'},
        't2': {'name': 'SQLMAP', 'icon': '💉', 'color': '#ff00ff'},
        't3': {'name': 'RCE TESTER', 'icon': '💻', 'color': '#ff6600'},
        't4': {'name': 'SSRF TESTER', 'icon': '🌐', 'color': '#00ffff'},
        't5': {'name': 'API & XSS', 'icon': '🔓', 'color': '#ffff00'},
        't6': {'name': 'LFI TESTER', 'icon': '📁', 'color': '#ff0066'}
    }
    
    cards_html = ""
    for term_id in ['t1', 't2', 't3', 't4', 't5', 't6']:
        data = results[term_id]
        info = terminal_info[term_id]
        
        status = data.get('status', 'waiting')
        vulns = data.get('vulnerabilities', [])
        log = data.get('log_preview', 'Initializing...')
        
        # Status display
        if status == 'completed':
            status_html = '<span style="color:#00ff00; font-weight:bold;">🟢 COMPLETED</span>'
        elif status == 'running':
            status_html = '<span style="color:#ffff00; font-weight:bold;">🟡 RUNNING</span>'
        elif status == 'error':
            status_html = '<span style="color:#ff0000; font-weight:bold;">🔴 ERROR</span>'
        else:
            status_html = '<span style="color:#888888;">⚪ WAITING</span>'
        
        # Stats
        stats = f'<div style="color:{info["color"]}; font-size:1.3em; font-weight:bold;">{len(vulns)} VULNERABILITIES</div>'
        if term_id == 't1' and 'open_ports' in data:
            stats += f'<div style="color:#00ff00; font-size:1.1em;">{len(data["open_ports"])} Ports Open</div>'
        if term_id == 't5' and 'endpoints_found' in data:
            stats += f'<div style="color:#ffff00; font-size:1.1em;">{len(data["endpoints_found"])} Endpoints</div>'
        
        # Vulnerability list (top 3)
        vulns_html = ""
        for v in vulns[:3]:
            sev = v.get('severity', 'Medium')
            color = {'Critical': '#ff0000', 'High': '#ff6600', 'Medium': '#ffff00', 'Low': '#00ff00'}.get(sev, '#ffff00')
            vulns_html += f'''
            <div style="border-left:4px solid {color}; padding:8px; margin:5px 0; background:#1a1a1a;">
                <strong style="color:{color}">[{sev}] {v.get("type", "Unknown")}</strong><br>
                <small style="color:#888;">{v.get("evidence", "N/A")[:80]}</small>
            </div>
            '''
        
        cards_html += f'''
        <div style="border:3px solid {info["color"]}; background:#111; padding:15px; margin:10px; border-radius:5px; min-width:350px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid {info["color"]}; padding-bottom:10px; margin-bottom:10px;">
                <span style="background:{info["color"]}; color:#000; padding:5px 15px; font-weight:bold; font-size:1.2em;">T{term_id[1]}</span>
                <span style="font-size:1.3em; font-weight:bold;">{info["icon"]} {info["name"]}</span>
                {status_html}
            </div>
            <div style="background:#000; border:1px solid #333; padding:10px; height:150px; overflow-y:auto; font-family:monospace; font-size:0.85em; color:#0f0; white-space:pre-wrap; margin-bottom:10px;">
                {log[:600]}
            </div>
            <div style="text-align:center; padding:10px; background:#0a0a0a; border-radius:3px;">
                {stats}
            </div>
            {vulns_html if vulns else '<div style="color:#666; text-align:center; margin-top:10px;">No vulnerabilities yet</div>'}
        </div>
        '''
    
    # Complete HTML
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>☠️ MrDos Attacked v2.0 - {target}</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{ font-family: 'Courier New', monospace; background: #050505; color: #00ff00; margin: 0; padding: 20px; }}
        .header {{ text-align: center; padding: 25px; border: 4px solid #00ff00; background: #0a0a0a; margin-bottom: 25px; }}
        .header h1 {{ font-size: 3em; text-shadow: 0 0 20px #00ff00; margin: 0; }}
        .stats-bar {{ display: flex; justify-content: center; gap: 50px; padding: 25px; background: #0f0f0f; border: 3px solid #00ff00; margin-bottom: 25px; }}
        .stat-box {{ text-align: center; }}
        .stat-number {{ font-size: 3.5em; font-weight: bold; color: #ffff00; text-shadow: 0 0 10px #ffff00; }}
        .terminals-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .footer {{ text-align: center; padding: 25px; border-top: 3px solid #00ff00; margin-top: 30px; color: #888; background: #0a0a0a; }}
        .update-time {{ text-align: center; color: #666; font-size: 0.9em; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>☠️ MrDos Attacked v2.0 ☠️</h1>
        <h2 style="color:#ffff00; margin:10px 0;">Penetration Testing Framework</h2>
        <p style="font-size:1.3em;">Target: <strong style="color:#ffff00; font-size:1.5em;">{target}</strong></p>
        <p style="color:#888;">Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats-bar">
        <div class="stat-box">
            <div class="stat-number">{total_vulns}</div>
            <div style="font-size:1.2em;">TOTAL VULNERABILITIES</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" style="color:#ff0000; text-shadow:0 0 10px #ff0000;">{critical}</div>
            <div style="color:#ff0000; font-size:1.2em;">CRITICAL</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" style="color:#ff6600;">{high}</div>
            <div style="color:#ff6600; font-size:1.2em;">HIGH</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" style="color:#00ffff;">{running}</div>
            <div style="color:#00ffff; font-size:1.2em;">RUNNING</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" style="color:#00ff00;">{completed}</div>
            <div style="color:#00ff00; font-size:1.2em;">COMPLETED</div>
        </div>
    </div>
    
    <div class="terminals-grid">
        {cards_html}
    </div>
    
    <div class="update-time">
        ⏱️ Last Updated: {datetime.now().strftime('%H:%M:%S')} | Auto-refresh: 5 seconds
    </div>
    
    <div class="footer">
        <p style="font-size:1.2em;">MrDos Attacked v2.0 | 6-Module Penetration Testing Framework</p>
        <p style="color:#ff6600; font-size:1.1em;">⚠️ For Authorized Security Testing Only</p>
        <p style="color:#666; margin-top:10px;">Modules: Nmap | SQLMap | RCE | SSRF | API/XSS | LFI</p>
    </div>
</body>
</html>'''
    
    # Save
    web_dir = os.path.join(workspace, 'web')
    os.makedirs(web_dir, exist_ok=True)
    
    dashboard_path = os.path.join(web_dir, 'index.html')
    with open(dashboard_path, 'w') as f:
        f.write(html)
    
    return dashboard_path

def main():
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "target.com"
    workspace = f"/tmp/mrdos_{target.replace('.', '_')}"
    
    print(f"[*] Generating dashboard for {target}...")
    path = generate_dashboard(workspace, target)
    print(f"[+] Dashboard: {path}")
    print(f"[+] Open: http://localhost:8888")

if __name__ == '__main__':
    main()
