from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)


EMAIL_ADDRESS = 'diasgeorgethomas@gmail.com'  
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') 

@app.route('/send-email', methods=['POST'])
def send_email():
    try:

        name = request.form['name']
        address = request.form['address']
        files = request.files.getlist('files')


        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'renjileon007@gmail.com'  
        msg['Subject'] = f'Email from {name}'


        body = f"Name: {name}\nAddress: {address}"
        msg.attach(MIMEText(body, 'plain'))


        for file in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {file.filename}')
            msg.attach(part)


        server = smtplib.SMTP('smtp.gmail.com', 587)  
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)


        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, 'renjileon007@gmail.com', text)
        server.quit()

        return jsonify({'message': 'Email sent successfully!'}), 200    

    except Exception as e:
        print(e)
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
