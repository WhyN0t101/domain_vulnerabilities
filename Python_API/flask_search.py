from flask import Flask, jsonify, make_response
from flask_caching import Cache
from flask_cors import CORS
import socket
import ssl
import dns.resolver
import requests
import hashlib
import OpenSSL
import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio
import re
import os

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})


# Thread pool executor for concurrency
executor = ThreadPoolExecutor(max_workers=10)

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = "API"

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

def resolve_domain(domain):
    if '.' not in domain:
        # Append a default TLD
        domain += '.pt'
    return domain

def is_valid_domain(domain):
    domain_regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,6})+$"
    return re.match(domain_regex, domain)

def check_dnssec_tlsa_with_recommendations(domain):
    resolver = dns.resolver.Resolver()
    result = {
        "dnssec_valid": False,
        "tlsa_records": []
    }
    recommendations = []
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

    if not result.get("dnssec_valid"):
        recommendations.append("DNSSEC is not enabled. Configure DNSSEC to improve domain security.")
    if not result.get("tlsa_records"):
        recommendations.append("No TLSA records found. Consider adding them for additional SSL validation.")

    result["recommendations"] = recommendations
    return result

def check_ssl_certificate(domain):
    result = {
        "certificate_valid": False,
        "certificate_issuer": None,
        "certificate_expiration": None,
        "certificate_chain": [],
        "ssl_error": None
    }
    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

        expiration_date = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
        result["certificate_expiration"] = expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        result["certificate_issuer"] = x509.get_issuer().CN if hasattr(x509.get_issuer(), 'CN') else str(x509.get_issuer())
        result["certificate_chain"].append(x509.get_subject().CN)

        if expiration_date > datetime.datetime.utcnow():
            result["certificate_valid"] = True
    except Exception as e:
        result["ssl_error"] = str(e)
    return result

def check_http_headers_with_recommendations(domain):
    result = {
        "content_security_policy": False,
        "x_content_type_options": False,
        "x_frame_options": False,
        "x_xss_protection": False,
        "permissions_policy": False,
        "referrer_policy": False,
        "security_score": 0
    }
    recommendations = []
    try:
        try:
            response = requests.get(f"http://{domain}", timeout=5, allow_redirects=True)
        except requests.exceptions.ConnectionError:
            # Retry with 'www.' prefix
            response = requests.get(f"http://www.{domain}", timeout=5, allow_redirects=True)

        headers = response.headers
        result["content_security_policy"] = 'Content-Security-Policy' in headers
        result["x_content_type_options"] = 'X-Content-Type-Options' in headers
        result["x_frame_options"] = 'X-Frame-Options' in headers
        result["x_xss_protection"] = 'X-XSS-Protection' in headers
        result["permissions_policy"] = 'Permissions-Policy' in headers
        result["referrer_policy"] = 'Referrer-Policy' in headers

        # Calculate a simple score
        result["security_score"] = sum(1 for key, value in result.items() if value is True)
    except Exception as e:
        result["error"] = str(e)

    if not result["content_security_policy"]:
        recommendations.append("Add a Content-Security-Policy header to mitigate cross-site scripting attacks.")
    if not result["x_content_type_options"]:
        recommendations.append("Add X-Content-Type-Options to prevent MIME-sniffing vulnerabilities.")
    if not result["x_frame_options"]:
        recommendations.append("Add X-Frame-Options to protect against clickjacking attacks.")
    if not result["x_xss_protection"]:
        recommendations.append("Add X-XSS-Protection to improve cross-site scripting (XSS) protection.")
    if not result["permissions_policy"]:
        recommendations.append("Add a Permissions-Policy header to restrict browser features.")
    if not result["referrer_policy"]:
        recommendations.append("Add a Referrer-Policy header to control referrer information sent with requests.")

    result["recommendations"] = recommendations
    return result

def check_vulnerabilities_with_recommendations(domain):
    try:
        # Example of a potential product detection (replace with actual detection logic)
        detected_software = "apache"  # Replace with server software for the domain

        # Query NVD API
        headers = {
            "User-Agent": "Domain-Vulnerability-Checker/1.0"
        }
        params = {
            "keywordSearch": detected_software,
            "resultsPerPage": 5,
            "startIndex": 0,
            "apiKey": NVD_API_KEY
        }
        response = requests.get(NVD_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        cve_data = response.json()
        if "vulnerabilities" in cve_data:
            cve_results = [
                {
                    "id": item["cve"]["id"],
                    "description": item["cve"]["descriptions"][0]["value"],
                    "severity": item.get("cve", {}).get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "Unknown")
                }
                for item in cve_data["vulnerabilities"]
            ]
            return {"cve_results": cve_results}
        else:
            return {"error": "No CVE data found for the given query."}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            return {"error": "Access forbidden. Ensure the API key is correct and rate limits are not exceeded."}
        return {"error": f"HTTP error occurred: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch CVE data: {e}"}



@app.route('/check_domain/<domain>', methods=['GET'])
@cache.cached(timeout=300)
async def check_domain(domain):
    domain = resolve_domain(domain)
    if not is_valid_domain(domain):
        return jsonify({"error": "Invalid domain name. Please use a fully qualified domain name."}), 400

    try:
        dnssec_tlsa = await run_in_executor(check_dnssec_tlsa_with_recommendations, domain)
        ssl_info = await run_in_executor(check_ssl_certificate, domain)
        http_headers = await run_in_executor(check_http_headers_with_recommendations, domain)
        vulnerabilities = await run_in_executor(check_vulnerabilities_with_recommendations, domain)

        response = {
            "domain": domain,
            "dnssec_tlsa": dnssec_tlsa,
            "ssl_info": ssl_info,
            "http_headers": http_headers,
            "vulnerabilities": vulnerabilities,
            "recommendations": {
                "dnssec": dnssec_tlsa.get("recommendations", []),
                "http_headers": http_headers.get("recommendations", []),
                "vulnerabilities": vulnerabilities.get("cve_results", [])
            }
        }

        res = make_response(jsonify(response))
        res.headers['Cache-Control'] = 'public, max-age=3600'
        res.headers['ETag'] = hashlib.md5(str(response).encode('utf-8')).hexdigest()
        return res
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
