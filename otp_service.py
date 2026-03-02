import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OTPService:
    def __init__(self):
        # Configuration - In a real prod environment, use environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "smartfruitai@gmail.com"
        self.app_password = "your_app_password" # To be configured by user

    def generate_otp(self):
        # DEMO MODE: Using fixed OTP for testing
        return "123456"

    def send_email_otp(self, receiver_email, otp):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "SmartFruit AI - Your Login OTP"

            body = f"""
            Hello,

            Your 6-digit verification code for SmartFruit AI is: {otp}

            This code will expire in 5 minutes. Do not share this code with anyone.

            Happy Farming!
            SmartFruit AI Team
            """
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            # server.login(self.sender_email, self.app_password) # Commented out until configured
            print(f"DEBUG: Email OTP {otp} sent to {receiver_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_sms_otp(self, phone_number, otp):
        # Mocking SMS provider
        print(f"--- MOCK SMS SERVICE ---")
        print(f"To: {phone_number}")
        print(f"Message: Your SmartFruit AI OTP is {otp}")
        print(f"------------------------")
        return True

otp_service = OTPService()
