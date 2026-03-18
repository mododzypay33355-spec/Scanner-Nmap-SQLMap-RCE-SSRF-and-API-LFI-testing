#!/usr/bin/env python3
"""TERMINAL 5: API & XSS SCANNER - Working Version"""
import os, sys, json, urllib.request, urllib.parse, urllib.error
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scan"
    
    print(f"[+] TERMINAL 5: API & XSS Scanner Started")
    print(f"[+] Target: {target}")
    
    os.makedirs(f"{workspace}/results", exist_ok=True)
    result_file = f"{workspace}/results/api_xss_scan.json"
    
    results = {"terminal": 5, "name": "API & XSS Scanner", "target": target,
        "start_time": datetime.now().isoformat(), "status": "running",
        "vulnerabilities": [], "endpoints_found": [], "log": ""}
    
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)
    
    # API Discovery
    api_paths = ['/api', '/api/v1', '/api/v2', '/rest', '/graphql', '/swagger', '/swagger.json', '/api-docs',
                 '/openapi.json', '/.env', '/config', '/api/users', '/api/login', '/api/admin',
                 '/wp-json', '/wp-json/wp/v2', '/json', '/xml', '/feed', '/rss', '/sitemap.xml']
    
    xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
                    "'\"><script>alert(1)</script>", "<svg onload=alert(1)>",
                    "javascript:alert('XSS')", "<body onload=alert('XSS')>"]
    
    log("[*] Discovering API endpoints...")
    
    for path in api_paths:
        url = f"http://{target}{path}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json,text/html'})
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                content = response.read().decode('utf-8', errors='ignore')
                
                if status == 200:
                    log(f"[+] Found endpoint: {url}")
                    results['endpoints_found'].append(url)
                    
                    # Check for exposed sensitive data
                    sensitive = ['password', 'secret', 'token', 'key', 'credentials', 'api_key', 'auth_token']
                    if any(s in content.lower() for s in sensitive):
                        log(f"[!] SENSITIVE DATA exposed at: {url}")
                        results['vulnerabilities'].append({
                            'type': 'Sensitive Data Exposure',
                            'severity': 'Critical',
                            'url': url,
                            'evidence': 'Response contains passwords/secrets'
                        })
                    
                    # Check for CORS misconfig
                    cors = response.headers.get('Access-Control-Allow-Origin', '')
                    if cors == '*':
                        log(f"[!] CORS Misconfiguration: {url}")
                        results['vulnerabilities'].append({
                            'type': 'CORS Misconfiguration',
                            'severity': 'Medium',
                            'url': url,
                            'evidence': 'Access-Control-Allow-Origin: *'
                        })
                        
        except urllib.error.HTTPError as e:
            if e.code == 401:
                log(f"[+] Protected endpoint: {url}")
                results['endpoints_found'].append(f"{url} (protected)")
        except: pass
    
    # XSS Testing
    log("[*] Testing for XSS...")
    xss_params = ['q', 'search', 'query', 'name', 'id', 'user', 'message', 'comment', 'input', 's']
    xss_urls = [f"http://{target}/", f"http://{target}/search", f"http://{target}/login", f"http://{target}/contact"]
    
    for base_url in xss_urls:
        for param in xss_params[:4]:
            for payload in xss_payloads[:3]:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                try:
                    req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10) as response:
                        content = response.read().decode('utf-8', errors='ignore')
                        
                        # Check if payload is reflected
                        if payload in content:
                            log(f"[!] XSS VULNERABILITY FOUND!")
                            log(f"  [+] URL: {test_url[:70]}")
                            log(f"  [+] Payload reflected: {payload[:30]}")
                            results['vulnerabilities'].append({
                                'type': 'Cross-Site Scripting (XSS)',
                                'severity': 'High',
                                'url': test_url,
                                'param': param,
                                'payload': payload,
                                'evidence': 'Payload reflected in response'
                            })
                            break
                except: pass
    
    results['status'] = 'completed'
    results['end_time'] = datetime.now().isoformat()
    results['log'] = '\n'.join(log_lines)
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"[+] API & XSS complete! {len(results['endpoints_found'])} endpoints, {len(results['vulnerabilities'])} vulns")

if __name__ == '__main__':
    main()
