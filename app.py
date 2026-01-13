import os
import msal
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# 1. Load configuration from your .env file
load_dotenv()
app = Flask(__name__)

def get_access_token():
    """
    Uses MSAL to log in independently using Client ID and Secret.
    """
    app_instance = msal.ConfidentialClientApplication(
        os.getenv("CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}",
        client_credential=os.getenv("CLIENT_SECRET")
    )
    # Requests a token for the Graph API using pre-configured permissions.
    result = app_instance.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Authentication Error: {result.get('error_description')}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-emails')
def get_emails():
    """
    Fetches the last 50 emails from the INBOX, sorted by date.
    """
    token = get_access_token()
    user_id = os.getenv("USER_ID")
    
    if not token:
        return jsonify({"status": "Error", "details": "Auth failed"}), 500

    # Increased $top to 50 and added $orderby for better list presentation
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/inbox/messages?$top=50&$select=id,subject,from,receivedDateTime&$orderby=receivedDateTime desc"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route('/get-sent')
def get_sent():
    """
    Fetches the last 50 emails from the SENT folder, sorted by date.
    """
    token = get_access_token()
    user_id = os.getenv("USER_ID")
    
    if not token:
        return jsonify({"status": "Error", "details": "Auth failed"}), 500

    # Increased $top to 50 and added $orderby
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/sentitems/messages?$top=50&$select=id,subject,toRecipients,receivedDateTime&$orderby=receivedDateTime desc"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route('/get-message/<msg_id>')
def get_message(msg_id):
    """
    Fetches the full content of a specific message for the popup modal.
    """
    token = get_access_token()
    user_id = os.getenv("USER_ID")
    
    if not token:
        return jsonify({"status": "Error", "details": "Auth failed"}), 500

    # Fetching the body (content), subject, and sender details
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{msg_id}?$select=subject,from,body,receivedDateTime"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Sends an email via Microsoft Graph API.
    """
    data = request.json
    token = get_access_token()
    user_id = os.getenv("USER_ID")
    
    if not token:
        return jsonify({"status": "Error", "details": "Auth failed"}), 500

    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/sendMail"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    email_payload = {
        "message": {
            "subject": data['subject'],
            "body": {"contentType": "HTML", "content": data['content']},
            "toRecipients": [{"emailAddress": {"address": data['to']}}]
        }
    }
    
    response = requests.post(url, headers=headers, json=email_payload)
    
    if response.status_code == 202:
        return jsonify({"status": "Success! Email sent."})
    return jsonify({"status": "Error", "details": response.text}), response.status_code

if __name__ == '__main__':
    # host='0.0.0.0' is critical for Docker/Kubernetes networking to work
    app.run(host='0.0.0.0', port=5750, debug=True)