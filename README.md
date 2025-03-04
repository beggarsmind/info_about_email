# info_about_email

Step 1: Install VS Code & Python
Install VS Code: https://code.visualstudio.com/
Install Python 3.x: https://www.python.org/downloads/
Verify installation:
sh
Copy
Edit
python --version
Step 2: Clone the Repository
Open VS Code Terminal (Ctrl + `)
Run:
sh
Copy
Edit
git clone https://github.com/beggarsmind/info_about_email.git
cd info_about_email
Step 3: Create & Activate Virtual Environment (Optional)
Create virtual environment:
sh
Copy
Edit
python -m venv venv
Activate virtual environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
Step 4: Install Required Libraries
sh
Copy
Edit
pip install -r requirements.txt
(If requirements.txt is missing, install manually:)

sh
Copy
Edit
pip install socket requests whois reportlab dnspython
Step 5: Add API Keys
Open info_about_email.py in VS Code
Replace:
python
Copy
Edit
HUNTER_API_KEY = "your_hunter_api_key"
CLEARBIT_API_KEY = "your_clearbit_api_key"
with your actual API keys.
Step 6: Run the Script
sh
Copy
Edit
python info_about_email.py
(or python3 info_about_email.py on macOS/Linux)

Step 7: Enter Email & View Results
Enter an email when prompted.
The script generates email_data_viewer.html.
Open email_data_viewer.html in a browser.
Step 8: Generate PDF (Optional)
The script generates example.pdf in the project folder.
