# custom_functions.py
"""
Custom pentesting functions for specialized tasks.
"""

import socket
import requests
import dns.resolver
import whois
import subprocess
import json
import re
import ipaddress
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional
from config import Colors, print_colored

class CustomPentestingFunctions:
    """Custom functions for specialized pentesting tasks."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def port_scan_basic(self, target: str, ports: List[int], timeout: int = 1) -> Dict[int, bool]:
        """Basic TCP port scanning."""
        print_colored(f"🔍 Scanning {len(ports)} ports on {target}", Colors.CYAN)
        results = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                results[port] = result == 0
                sock.close()
                
                if results[port]:
                    print_colored(f"   ✅ Port {port}/tcp open", Colors.GREEN)
                    
            except Exception as e:
                results[port] = False
                print_colored(f"   ❌ Error scanning port {port}: {e}", Colors.RED)
        
        return results
    
    def web_technology_detection(self, url: str) -> Dict[str, Any]:
        """Detect web technologies and gather basic info."""
        print_colored(f"🌐 Analyzing web technologies for {url}", Colors.CYAN)
        
        results = {
            'url': url,
            'status_code': None,
            'headers': {},
            'technologies': [],
            'security_headers': {},
            'forms': [],
            'links': []
        }
        
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            results['status_code'] = response.status_code
            results['headers'] = dict(response.headers)
            
            # Check for common technologies
            content = response.text.lower()
            tech_patterns = {
                'WordPress': ['wp-content', 'wp-includes'],
                'Drupal': ['drupal', '/sites/default/'],
                'Joomla': ['joomla', '/components/com_'],
                'Apache': ['apache'],
                'Nginx': ['nginx'],
                'PHP': ['php', '.php'],
                'ASP.NET': ['asp.net', '__viewstate'],
                'jQuery': ['jquery'],
                'Bootstrap': ['bootstrap']
            }
            
            for tech, patterns in tech_patterns.items():
                if any(pattern in content for pattern in patterns):
                    results['technologies'].append(tech)
            
            # Security headers analysis
            security_headers = [
                'x-frame-options', 'x-content-type-options', 'x-xss-protection',
                'strict-transport-security', 'content-security-policy',
                'x-powered-by', 'server'
            ]
            
            for header in security_headers:
                value = response.headers.get(header)
                if value:
                    results['security_headers'][header] = value
            
            # Basic form detection
            form_pattern = r'<form[^>]*>(.*?)</form>'
            forms = re.findall(form_pattern, content, re.IGNORECASE | re.DOTALL)
            results['forms'] = len(forms)
            
            print_colored(f"   ✅ Status: {results['status_code']}", Colors.GREEN)
            print_colored(f"   🔧 Technologies: {', '.join(results['technologies'])}", Colors.YELLOW)
            
        except Exception as e:
            print_colored(f"   ❌ Error analyzing {url}: {e}", Colors.RED)
            results['error'] = str(e)
        
        return results
    
    def dns_enumeration(self, domain: str) -> Dict[str, Any]:
        """Comprehensive DNS enumeration."""
        print_colored(f"🔍 DNS enumeration for {domain}", Colors.CYAN)
        
        results = {
            'domain': domain,
            'a_records': [],
            'aaaa_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'cname_records': [],
            'subdomains': []
        }
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records = [str(rdata) for rdata in answers]
                results[f'{record_type.lower()}_records'] = records
                print_colored(f"   ✅ {record_type}: {len(records)} records", Colors.GREEN)
            except Exception:
                print_colored(f"   ⚠️  No {record_type} records found", Colors.YELLOW)
        
        # Common subdomain enumeration
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
            'blog', 'shop', 'portal', 'secure', 'vpn', 'remote'
        ]
        
        for subdomain in common_subdomains:
            try:
                full_domain = f"{subdomain}.{domain}"
                dns.resolver.resolve(full_domain, 'A')
                results['subdomains'].append(full_domain)
                print_colored(f"   ✅ Found subdomain: {full_domain}", Colors.GREEN)
            except:
                pass
        
        return results
    
    def whois_lookup(self, domain: str) -> Dict[str, Any]:
        """WHOIS information gathering."""
        print_colored(f"📋 WHOIS lookup for {domain}", Colors.CYAN)
        
        try:
            w = whois.whois(domain)
            results = {
                'domain': domain,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'name_servers': w.name_servers if w.name_servers else [],
                'status': w.status if w.status else [],
                'emails': w.emails if w.emails else []
            }
            
            print_colored(f"   ✅ Registrar: {results['registrar']}", Colors.GREEN)
            print_colored(f"   📅 Creation: {results['creation_date']}", Colors.YELLOW)
            
            return results
            
        except Exception as e:
            print_colored(f"   ❌ WHOIS lookup failed: {e}", Colors.RED)
            return {'domain': domain, 'error': str(e)}
    
    def vulnerability_check_basic(self, url: str) -> Dict[str, Any]:
        """Basic vulnerability checks."""
        print_colored(f"🔒 Basic vulnerability assessment for {url}", Colors.CYAN)
        
        results = {
            'url': url,
            'vulnerabilities': [],
            'security_issues': [],
            'recommendations': []
        }
        
        try:
            response = self.session.get(url, timeout=10)
            headers = response.headers
            content = response.text
            
            # Check for common security issues
            checks = {
                'Missing X-Frame-Options': 'x-frame-options' not in headers,
                'Missing X-Content-Type-Options': 'x-content-type-options' not in headers,
                'Missing X-XSS-Protection': 'x-xss-protection' not in headers,
                'Server header disclosure': 'server' in headers,
                'X-Powered-By disclosure': 'x-powered-by' in headers,
                'Directory listing enabled': 'index of' in content.lower(),
                'Default pages present': any(x in content.lower() for x in ['apache2 ubuntu default', 'welcome to nginx']),
                'Potential SQL injection points': '?' in url and any(x in url.lower() for x in ['id=', 'user=', 'page=']),
                'HTTP instead of HTTPS': url.startswith('http://'),
            }
            
            for issue, condition in checks.items():
                if condition:
                    results['security_issues'].append(issue)
                    print_colored(f"   ⚠️  {issue}", Colors.YELLOW)
            
            # Generate recommendations
            if 'Missing X-Frame-Options' in results['security_issues']:
                results['recommendations'].append('Add X-Frame-Options header to prevent clickjacking')
            
            if 'HTTP instead of HTTPS' in results['security_issues']:
                results['recommendations'].append('Implement HTTPS/TLS encryption')
            
            if 'Server header disclosure' in results['security_issues']:
                results['recommendations'].append('Hide server version information')
            
        except Exception as e:
            print_colored(f"   ❌ Vulnerability check failed: {e}", Colors.RED)
            results['error'] = str(e)
        
        return results
    
    def network_discovery(self, network_range: str) -> List[str]:
        """Discover live hosts in network range."""
        print_colored(f"🔍 Network discovery for {network_range}", Colors.CYAN)
        
        live_hosts = []
        
        try:
            network = ipaddress.IPv4Network(network_range, strict=False)
            
            for ip in network.hosts():
                ip_str = str(ip)
                try:
                    # Simple ping check
                    result = subprocess.run(
                        ['ping', '-c', '1', '-W', '1000', ip_str],
                        capture_output=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        live_hosts.append(ip_str)
                        print_colored(f"   ✅ Host alive: {ip_str}", Colors.GREEN)
                        
                except:
                    pass
                    
        except Exception as e:
            print_colored(f"   ❌ Network discovery failed: {e}", Colors.RED)
        
        print_colored(f"   📊 Found {len(live_hosts)} live hosts", Colors.CYAN)
        return live_hosts
    
    def generate_report(self, findings: Dict[str, Any]) -> str:
        """Generate a comprehensive penetration testing report."""
        print_colored("📊 Generating penetration testing report...", Colors.CYAN, bold=True)
        
        report = f"""
PENETRATION TESTING REPORT
{'=' * 50}

Target Information:
- Target: {findings.get('target', 'N/A')}
- Scan Date: {findings.get('scan_date', 'N/A')}
- Methodology: OWASP Testing Guide / PTES

Executive Summary:
{findings.get('executive_summary', 'Comprehensive security assessment performed.')}

Findings Summary:
- Critical: {len([f for f in findings.get('vulnerabilities', []) if f.get('severity') == 'Critical'])}
- High: {len([f for f in findings.get('vulnerabilities', []) if f.get('severity') == 'High'])}
- Medium: {len([f for f in findings.get('vulnerabilities', []) if f.get('severity') == 'Medium'])}
- Low: {len([f for f in findings.get('vulnerabilities', []) if f.get('severity') == 'Low'])}

Detailed Findings:
"""
        
        for i, vuln in enumerate(findings.get('vulnerabilities', []), 1):
            report += f"""
{i}. {vuln.get('title', 'Vulnerability')}
   Severity: {vuln.get('severity', 'Unknown')}
   Description: {vuln.get('description', 'No description')}
   Recommendation: {vuln.get('recommendation', 'Review and remediate')}
   
"""
        
        report += f"""
Technical Details:
{findings.get('technical_details', 'See individual command outputs for technical details.')}

Recommendations:
{chr(10).join([f"- {rec}" for rec in findings.get('recommendations', [])])}

Tools Used:
{chr(10).join([f"- {tool}" for tool in findings.get('tools_used', [])])}

Report Generated by: AutoPentest AI Agent
"""
        
        return report

# Global custom functions instance
custom_functions = CustomPentestingFunctions()
