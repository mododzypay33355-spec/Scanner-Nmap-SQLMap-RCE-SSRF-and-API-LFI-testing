#!/usr/bin/env python3
"""TERMINAL 1: NMAP PORT SCANNER - Working Version"""
import os
import sys
import json
import subprocess
import socket
from datetime import datetime

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scan"
    
    try:
        target_ip = socket.gethostbyname(target)
    except:
        target_ip = target
    
    print(f"[+] TERMINAL 1: Nmap Scanner Started")
    print(f"[+] Target: {target} ({target_ip})")
    
    os.makedirs(f"{workspace}/results", exist_ok=True)
    result_file = f"{workspace}/results/nmap_scan.json"
    
    results = {
        "terminal": 1,
        "name": "Nmap Scanner",
        "target": target,
        "target_ip": target_ip,
        "start_time": datetime.now().isoformat(),
        "status": "running",
        "open_ports": [],
        "services": {},
        "vulnerabilities": [],
        "log": ""
    }
    
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)
    
    log("[*] Starting port discovery...")
    
    try:
        # Quick port scan
        cmd = ["nmap", "-p-", "--open", "-T4", "--max-retries", "1", "--max-rtt-timeout", "500ms", target_ip]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout
        
        for line in output.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                port = parts[0].split('/')[0]
                service = parts[2] if len(parts) > 2 else "unknown"
                results['open_ports'].append(int(port))
                results['services'][port] = service
                log(f"  [+] Port {port}/tcp open - {service}")
        
        log(f"[*] Found {len(results['open_ports'])} open ports")
        
        # Service detection
        if results['open_ports']:
            log("[*] Detecting services...")
            ports_str = ','.join(map(str, results['open_ports']))
            cmd2 = ["nmap", "-p", ports_str, "-sV", "-T4", target_ip]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
            
            output_lower = result2.stdout.lower()
            
            if 'mysql' in output_lower or 'mariadb' in output_lower:
                results['vulnerabilities'].append({
                    'type': 'Exposed Database',
                    'severity': 'Critical',
                    'port': '3306',
                    'evidence': 'MySQL/MariaDB found on open port'
                })
                log("[!] CRITICAL: Exposed database found!")
            
            if 'ftp' in output_lower:
                results['vulnerabilities'].append({
                    'type': 'Exposed FTP',
                    'severity': 'High',
                    'port': '21',
                    'evidence': 'FTP service exposed'
                })
                log("[!] HIGH: FTP service exposed!")
            
            if 'ssh' in output_lower:
                log("[+] SSH service detected")
            
            if 'http' in output_lower:
                log("[+] HTTP service detected")
        
        results['status'] = 'completed'
        
    except subprocess.TimeoutExpired:
        log("[!] Nmap scan timed out")
        results['status'] = 'timeout'
    except Exception as e:
        log(f"[!] Error: {e}")
        results['status'] = f'error: {str(e)}'
    
    results['end_time'] = datetime.now().isoformat()
    results['log'] = '\n'.join(log_lines)
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    log(f"[+] Nmap complete! {len(results['open_ports'])} ports, {len(results['vulnerabilities'])} vulns")

if __name__ == '__main__':
    main()
