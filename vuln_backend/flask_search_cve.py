import os
import logging
from flask import Flask, jsonify, make_response
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import socket
import ssl
import dns.resolver
import requests
import hashlib
import OpenSSL
import datetime
from datetime import timezone
from concurrent.futures import ThreadPoolExecutor
import asyncio
import validators
from builtwith import builtwith
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

# Configuration
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)
CORS(app, resources={r"/*": {"origins": "*"}})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Thread pool executor for concurrency
executor = ThreadPoolExecutor(max_workers=10)

# Environment variables

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

def resolve_domain(domain):
    if '.' not in domain:
        domain += '.pt'
    return domain

def is_valid_domain(domain):
    return validators.domain(domain)

def detect_technologies_with_builtwith(domain):
    try:
        tech = builtwith(f"https://{domain}")
        if not isinstance(tech, dict):
            raise ValueError("BuiltWith returned unexpected data format.")
        return tech
    except Exception as e:
        return {"error": str(e)}

def fetch_headers(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=False)
        return dict(response.headers)
    except Exception as e:
        return {"error": str(e)}

def detect_versions_from_html(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_generator = soup.find("meta", {"name": "generator"})
        generator_content = meta_generator["content"] if meta_generator else "Unknown"

        return {"meta_generator": generator_content}
    except Exception as e:
        return {"error": str(e)}
def fetch_cves(technology, version=None):
    """
    Fetch CVEs for a specific technology and version, extracting relevant information.
    """
    try:
        params = {
            "keywordSearch": f"{technology} {version}" if version else technology,
            "resultsPerPage": 10  # Fetch only top 10 CVEs
        }
        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0", params=params, timeout=10)
        response.raise_for_status()
        cve_data = response.json()
        cves = cve_data.get("vulnerabilities", [])
        
        # Extract relevant information
        extracted_cves = []
        for cve_entry in cves:
            cve = cve_entry.get("cve", {})
            metrics = cve.get("metrics", {})
            
            # Extract severity from cvssMetricV3 or fallback to cvssMetricV2
            severity = None
            if "cvssMetricV3" in metrics:
                severity = metrics["cvssMetricV3"][0]["cvssData"].get("baseScore", "Unknown")
            elif "cvssMetricV2" in metrics:
                severity = metrics["cvssMetricV2"][0]["cvssData"].get("baseScore", "Unknown")
            
            # Extract description (in English)
            description = next((desc["value"] for desc in cve.get("descriptions", []) if desc["lang"] == "en"), "No description available.")
            
            # Append parsed CVE details
            extracted_cves.append({
                "id": cve.get("id"),
                "severity": severity,
                "description": description
            })

        return extracted_cves
    except Exception as e:
        return {"error": f"Error fetching CVEs: {e}"}



def get_cves_for_domain(domain):
    detected_tech = detect_technologies_with_builtwith(domain)
    headers = fetch_headers(domain)
    meta_versions = detect_versions_from_html(domain)

    results = {"technologies": detected_tech, "cves": {}}

    for tech in detected_tech.keys():
        version = None
        if "Server" in headers and tech.lower() in headers["Server"].lower():
            version = headers["Server"].split("/")[-1]
        elif meta_versions.get("meta_generator") and tech.lower() in meta_versions["meta_generator"].lower():
            version = meta_versions["meta_generator"].split()[-1]

        cves = fetch_cves(tech, version)
        results["cves"][tech] = {"version": version, "cves": cves}

    return results


def deduplicate_remediation_links(cves):
    """
    Deduplicate remediation links in CVE entries and ensure consistent formatting.
    """
    for tech, cve_list in cves.items():
        for cve in cve_list:
            if "remediation" in cve:
                # Deduplicate and sort the remediation URLs
                links = list(set(cve["remediation"].split(", ")))
                cve["remediation"] = ", ".join(sorted(links))
    return cves


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
            recommendations.append("No TLSA records found. Configure TLSA for better SSL validation.")
        except dns.resolver.NXDOMAIN:
            recommendations.append(f"No DNS records found for {domain}. Ensure your DNS is properly configured.")
    except Exception as e:
        logger.error(f"DNSSEC/TLSA check failed for {domain}: {e}")
        result["error"] = str(e)

    if not result.get("dnssec_valid"):
        recommendations.append("DNSSEC is not enabled. Configure DNSSEC to improve domain security.")

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
        expiration_date = expiration_date.replace(tzinfo=timezone.utc)
        result["certificate_expiration"] = expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        result["certificate_issuer"] = x509.get_issuer().CN if hasattr(x509.get_issuer(), 'CN') else str(x509.get_issuer())
        result["certificate_chain"].append(x509.get_subject().CN)

        if expiration_date > datetime.datetime.now(timezone.utc):
            result["certificate_valid"] = True
    except Exception as e:
        logger.error(f"SSL certificate check failed for {domain}: {e}")
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
            response = requests.get(f"https://{domain}", timeout=5, allow_redirects=True, verify=False)
        except requests.exceptions.ConnectionError:
            response = requests.get(f"http://{domain}", timeout=5, allow_redirects=True, verify=False)

        headers = response.headers
        result["content_security_policy"] = 'Content-Security-Policy' in headers
        result["x_content_type_options"] = 'X-Content-Type-Options' in headers
        result["x_frame_options"] = 'X-Frame-Options' in headers
        result["x_xss_protection"] = 'X-XSS-Protection' in headers
        result["permissions_policy"] = 'Permissions-Policy' in headers
        result["referrer_policy"] = 'Referrer-Policy' in headers

        result["security_score"] = sum(1 for key, value in result.items() if value is True)
    except Exception as e:
        logger.error(f"HTTP header check failed for {domain}: {e}")
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

@app.route('/check_domain/<domain>', methods=['GET'])
@cache.cached(timeout=300)
@limiter.limit("10 per minute")
async def check_domain(domain):
    domain = resolve_domain(domain)
    if not is_valid_domain(domain):
        return jsonify({"error": "Invalid domain name. Please use a fully qualified domain name."}), 400

    try:
        dnssec_tlsa = await run_in_executor(check_dnssec_tlsa_with_recommendations, domain)
        ssl_info = await run_in_executor(check_ssl_certificate, domain)
        http_headers = await run_in_executor(check_http_headers_with_recommendations, domain)
        tech_cves = await run_in_executor(get_cves_for_domain, domain)

        # Consolidate recommendations
        all_recommendations = list(set(
            dnssec_tlsa.get("recommendations", []) +
            http_headers.get("recommendations", [])
        ))

        # Separate vulnerabilities
        vulnerabilities = tech_cves.get("cves", {})

        # Format the response
        response = {
            "domain": domain,
            "dnssec_tlsa": dnssec_tlsa,
            "ssl_info": ssl_info,
            "http_headers": http_headers,
            "recommendations": {
                "all": all_recommendations
            },
            "vulnerabilities": vulnerabilities
        }

        res = make_response(jsonify(response))
        res.headers['Cache-Control'] = 'public, max-age=3600'
        res.headers['ETag'] = hashlib.md5(str(response).encode('utf-8')).hexdigest()
        return res
    except Exception as e:
        logger.error(f"Unexpected error for {domain}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)