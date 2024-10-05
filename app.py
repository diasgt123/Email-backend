from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurations for the email
EMAIL_ADDRESS = 'diasgeorgethomas@gmail.com'  # Replace with your email
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Load password from environment variable

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Get form data
        name = request.form['name']
        address = request.form['address']
        files = request.files.getlist('files')

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'renjileon007@gmail.com'  # The owner's email
        msg['Subject'] = f'Email from {name}'

        # Add text content to the email
        body = f"Name: {name}\nAddress: {address}"
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        for file in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {file.filename}')
            msg.attach(part)

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Ethereal or any SMTP service
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, 'renjileon007@gmail.com', text)
        server.quit()

        return jsonify({'message': 'Email sent successfully!'}), 200    

    except Exception as e:
        print(e)
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
