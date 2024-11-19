import concurrent.futures
import socket
import ssl
import dns.resolver
import requests
import hashlib
import OpenSSL
import datetime
import nmap
from flask import Flask, jsonify, make_response
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

# Enable CORS for all routes
CORS(app)

# Utility function: DNSSEC and TLSA records
def check_dnssec_tlsa(domain):
    resolver = dns.resolver.Resolver()
    result = {
        "dnssec_valid": False,
        "tlsa_records": []
    }
    try:
        dnssec_query = resolver.resolve(domain, 'A', raise_on_no_answer=False)
        result["dnssec_valid"] = dnssec_query.response.flags & 0x20 != 0  # AD flag for DNSSEC validation
        try:
            tlsa_records = resolver.resolve(f"_443._tcp.{domain}", "TLSA")
            result["tlsa_records"] = [rdata.to_text() for rdata in tlsa_records]
        except dns.resolver.NoAnswer:
            result["tlsa_records"] = []
    except Exception as e:
        result["error"] = str(e)
    return result

def check_ssl_certificate(domain):
    result = {
        "certificate_valid": False,
        "certificate_issuer": None,
        "certificate_expiration": None,
        "ssl_error": None
    }
    try:
        # Get the certificate from the domain
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

        # Validate the certificate expiration date
        expiration_date = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
        result["certificate_expiration"] = expiration_date.strftime('%Y-%m-%d %H:%M:%S')

        if expiration_date > datetime.datetime.utcnow():
            result["certificate_valid"] = True
        
        result["certificate_issuer"] = x509.get_issuer()
    except Exception as e:
        result["ssl_error"] = str(e)

    return result

def check_https(domain):
    result = {
        "redirects_to_https": False,
        "hsts_supported": False,
        "ssl_versions_supported": [],
        "weak_ssl_v3": False,
        "ssl_certificate": {}
    }
    try:
        # Check HTTPS redirection and HSTS
        response = requests.get(f"http://{domain}", timeout=5, allow_redirects=True)
        result["redirects_to_https"] = response.url.startswith("https://")
        if "Strict-Transport-Security" in response.headers:
            result["hsts_supported"] = True

        # Check SSL/TLS versions with relaxed hostname checking
        context = ssl.create_default_context()
        context.check_hostname = False  # Skip hostname verification
        for version in [ssl.PROTOCOL_TLSv1_2, ssl.PROTOCOL_TLSv1_3]:
            try:
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        if version in ssock.version():
                            result["ssl_versions_supported"].append(ssock.version())
            except Exception:
                continue

        # Check for SSLv3 vulnerability (POODLE)
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable SSLv2 and SSLv3
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                if ssock.version() == 'SSLv3':
                    result["weak_ssl_v3"] = True

        # SSL Certificate details
        result["ssl_certificate"] = check_ssl_certificate(domain)
    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL error: {e}"
    except Exception as e:
        result["error"] = str(e)
    return result

# Utility function: Email Security
def check_email_security(domain):
    result = {
        "spf_record": None,
        "dmarc_record": None,
        "dkim_supported": False,
        "starttls_supported": False,
        "dane_tlsa": []
    }
    resolver = dns.resolver.Resolver()

    try:
        # SPF record
        spf_query = resolver.resolve(domain, "TXT", raise_on_no_answer=False)
        result["spf_record"] = next((rdata.to_text() for rdata in spf_query if "v=spf1" in rdata.to_text()), None)

        # DMARC record
        dmarc_query = resolver.resolve(f"_dmarc.{domain}", "TXT", raise_on_no_answer=False)
        result["dmarc_record"] = next((rdata.to_text() for rdata in dmarc_query), None)

        # STARTTLS support
        mail_server_query = resolver.resolve(domain, "MX", raise_on_no_answer=False)
        mail_server = sorted([(r.preference, r.exchange.to_text()) for r in mail_server_query])[0][1]
        with socket.create_connection((mail_server, 25), timeout=5) as sock:
            sock.recv(1024)
            sock.send(b"EHLO test\r\n")
            response = sock.recv(1024).decode()
            result["starttls_supported"] = "STARTTLS" in response

        # DANE (TLSA) records for email
        dane_query = resolver.resolve(f"_25._tcp.{domain}", "TLSA", raise_on_no_answer=False)
        result["dane_tlsa"] = [rdata.to_text() for rdata in dane_query]
    except Exception as e:
        result["error"] = str(e)
    return result

# Utility function to check HTTP Security Headers
def check_http_security_headers(domain):
    result = {
        "content_security_policy": False,
        "x_content_type_options": False,
        "x_frame_options": False,
        "x_xss_protection": False,
        "x_download_options": False,
        "strict_transport_security": False,
        "referrer_policy": False,
    }
    
    try:
        # Send a request to the domain to check headers
        response = requests.get(f"http://{domain}", timeout=5, allow_redirects=True)
        
        # Check if the headers exist
        result["content_security_policy"] = 'Content-Security-Policy' in response.headers
        result["x_content_type_options"] = 'X-Content-Type-Options' in response.headers
        result["x_frame_options"] = 'X-Frame-Options' in response.headers
        result["x_xss_protection"] = 'X-XSS-Protection' in response.headers
        result["x_download_options"] = 'X-Download-Options' in response.headers
        result["strict_transport_security"] = 'Strict-Transport-Security' in response.headers
        result["referrer_policy"] = 'Referrer-Policy' in response.headers
        
    except requests.exceptions.RequestException as e:
        result["error"] = f"HTTP request failed: {e}"
    
    return result

# Utility function to perform a basic vulnerability scan
def perform_vulnerability_scan(domain):
    result = {
        "vulnerabilities": []
    }
    
    try:
        # Perform a basic Nmap scan
        nm = nmap.PortScanner()
        nm.scan(domain, '1-1024')
        
        # Check for open ports and services
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = sorted(nm[host][proto].keys())
                for port in lport:
                    result["vulnerabilities"].append({
                        "port": port,
                        "protocol": proto,
                        "service": nm[host][proto][port]['name'],
                        "version": nm[host][proto][port]['version']
                    })
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

# Function to create an ETag from response data
def generate_etag(data):
    return hashlib.md5(str(data).encode('utf-8')).hexdigest()

# API Endpoint
@app.route('/check_domain/<domain>', methods=['GET'])
@cache.cached(timeout=300)  # Cache the response for 5 minutes (300 seconds)
def check_domain(domain):
    try:
        dnssec_tlsa_info = check_dnssec_tlsa(domain)
        https_info = check_https(domain)
        email_info = check_email_security(domain)
        http_security_headers = check_http_security_headers(domain)
        vulnerability_scan = perform_vulnerability_scan(domain)

        response = {
            "domain": domain,
            "dnssec_tlsa": dnssec_tlsa_info,
            "https": https_info,
            "email_security": email_info,
            "http_security_headers": http_security_headers,
            "vulnerability_scan": vulnerability_scan
        }

        # Create a response object
        res = make_response(jsonify(response))

        # Set Cache-Control headers (public and cache for 1 hour)
        res.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
        res.headers['ETag'] = generate_etag(response)  # ETag for cache validation

        return res
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to parallelize the checks
def parallelize_checks(domains):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(check_domain, domain) for domain in domains]
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
        return results

# API Endpoint to check multiple domains
@app.route('/check_domains', methods=['POST'])
def check_domains():
    try:
        domains = request.json['domains']
        results = parallelize_checks(domains)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
