# 🚀 Graph Mailer Pro

Graph Mailer Pro is a professional-grade web application built with Python (Flask) and Microsoft Graph API. It features a responsive dashboard to send emails and view your Inbox and Outbox (Sent Items) using a secure, containerized environment.

## 🛠 Features
- **Modern UI**: Professional 45/55 split-screen layout for desktop.
- **Mobile Optimized**: Responsive design specifically scaled for cellular phone screens.
- **Microsoft Graph Integration**: Securely connects to Microsoft Entra for mail operations.
- **Dockerized**: Fully containerized for easy deployment and environment consistency.

---

## 🔐 Prerequisites & App Registration

To run this app, you need to register it in the Microsoft Entra admin center:

1. **Register Your App**: Go to the [Microsoft Entra App Registrations](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsPyBlade).
2. **API Permissions**: Ensure the app has `Mail.Send` and `Mail.Read` (Application type) permissions.
3. **Admin Consent**: Click 'Grant admin consent' for your organization.
4. **Credentials**: Generate a **Client Secret** and copy your **Tenant ID** and **Client ID**.

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/graph-mailer-pro.git](https://github.com/yourusername/graph-mailer-pro.git)
cd graph-mailer-pro
2. Configure Environment Variables
Copy the example environment file and fill in your credentials:

Bash

cp .env.example .env
Edit .env and fill in your specific IDs. Note: Never commit your .env file to version control.

3. Install Dependencies
Bash

pip install -r requirements.txt
4. Run the App
Bash

python app.py
Access the app at http://localhost:5750.

🐳 Docker Deployment
The most reliable way to run Graph Mailer Pro is using Docker.

1. Build the Image
Bash

docker build -t graph-mailer-pro .
2. Run the Container
Bash

docker run -d -p 5750:5750 --name mailer-app --env-file .env graph-mailer-pro
3. Manage the Container
View Logs: docker logs -f mailer-app

Stop App: docker stop mailer-app

Restart App: docker restart mailer-app

📁 Project Structure
app.py: Main Flask backend with Microsoft Graph logic.

templates/index.html: Responsive frontend UI.

Dockerfile: Container configuration.

.env.example: Template for required security credentials.

.dockerignore / .gitignore: Rules to keep secrets and temporary files out of the project.

📝 License
This project is licensed under the MIT License.