import socket
import dns.resolver
import requests
import whois
from reportlab.pdfgen import canvas

# Hunter.io API Key (replace with your API key)
HUNTER_API_KEY = "your_hunter_api_key"

# Clearbit API Key (replace with your API key)
CLEARBIT_API_KEY = "your_clearbit_api_key"

def get_email_domain(email):
    """Extract the domain from an email address."""
    try:
        return email.split('@')[1]
    except IndexError:
        return None

def get_ip_from_domain(domain):
    """Get the IP address of a domain."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_mx_records(domain):
    """Get MX records for a domain."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [f"{record.preference}: {record.exchange}" for record in answers]
    except Exception as e:
        return [f"Error: {str(e)}"]

def get_spf_record(domain):
    """Get SPF record for a domain."""
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for record in answers:
            txt_data = record.to_text()
            if "v=spf1" in txt_data:
                return txt_data
        return "No SPF record found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_geolocation(ip):
    """Get geolocation of an IP using a public API."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

def validate_email_with_hunter(email):
    """Validate email using Hunter.io API."""
    try:
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_owner_info_with_clearbit(email):
    """Get owner information using Clearbit API."""
    headers = {"Authorization": f"Bearer {CLEARBIT_API_KEY}"}
    url = f"https://person.clearbit.com/v2/combined/find?email={email}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Unable to fetch owner info: {response.status_code}"}

def get_whois_info(domain):
    """Get WHOIS information for a domain."""
    try:
        return whois.whois(domain)
    except Exception as e:
        return {"error": str(e)}

def generate_html(email, domain, ip_address, mx_records, spf_record, geolocation, hunter_validation, clearbit_info, whois_info):
    """Generate an HTML file to display the data."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Data Viewer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                padding: 20px;
                margin: 0;
                background-color: #f9f9f9;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                max-width: 800px;
                border-collapse: collapse;
                margin-bottom: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .container {{
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
            }}
            .download-btn {{
                display: block;
                width: 200px;
                margin: 20px auto;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .download-btn:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Email Data Viewer</h1>
            <table>
                <tr><th>Field</th><th>Details</th></tr>
                <tr><td>Email</td><td>{email}</td></tr>
                <tr><td>Domain</td><td>{domain}</td></tr>
                <tr><td>IP Address</td><td>{ip_address or "N/A"}</td></tr>
            </table>
            <h2>MX Records</h2>
            <table>
                <tr><th>Priority</th><th>Mail Server</th></tr>
                {"".join(f"<tr><td>{record.split(':')[0]}</td><td>{record.split(':')[1]}</td></tr>" for record in mx_records)}
            </table>
            <h2>SPF Record</h2>
            <p>{spf_record}</p>
            <h2>Geolocation Details</h2>
            <table>
                <tr><th>Field</th><th>Details</th></tr>
                {"".join(f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>" for key, value in (geolocation or {}).items())}
            </table>
            <h2>Email Validation (Hunter.io)</h2>
            <table>
                <tr><th>Field</th><th>Details</th></tr>
                {"".join(f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>" for key, value in hunter_validation.get("data", {}).items()) if "data" in hunter_validation else f"<tr><td colspan='2'>{hunter_validation.get('error', 'No data available')}</td></tr>"}
            </table>
            <h2>Owner Information (Clearbit)</h2>
            <table>
                {"".join(f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>" for key, value in clearbit_info.get("person", {}).items()) if "person" in clearbit_info else f"<tr><td colspan='2'>{clearbit_info.get('error', 'No data available')}</td></tr>"}
                {"".join(f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>" for key, value in clearbit_info.get("company", {}).items()) if "company" in clearbit_info else ""}
            </table>
            <h2>WHOIS Info</h2>
            <table>
                {"".join(f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>" for key, value in whois_info.items())}
            </table>
            <button class="download-btn" onclick="generate_pdf()">Download as PDF</button>
        </div>
    </body>
    </html>
    """
    with open("email_data_viewer.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML file 'email_data_viewer.html' has been created.")

def generate_pdf():
    c = canvas.Canvas("example.pdf")
    c.drawString(100, 750, "Hello World")
    c.save()

# Main script
email = input("Enter the email ID: ")
domain = get_email_domain(email)

if domain:
    ip_address = get_ip_from_domain(domain)

    # Additional data
    mx_records = get_mx_records(domain)
    spf_record = get_spf_record(domain)
    geolocation = get_geolocation(ip_address)
    hunter_validation = validate_email_with_hunter(email)
    clearbit_info = get_owner_info_with_clearbit(email)
    whois_info = get_whois_info(domain)

    # Generate HTML file
    generate_html(email, domain, ip_address, mx_records, spf_record, geolocation, hunter_validation, clearbit_info, whois_info)

else:
    print("Invalid email ID.")
