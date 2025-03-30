import streamlit as st
from notifiers.email_notifier import EmailNotifier
from views.menu_view import menu_view
from config import config
from dotenv import load_dotenv
import os

config.setup_app()
load_dotenv()

def main():
    st.title("Alert System Dashboard")
    
    # Crear el notificador de correos con las credenciales del archivo .env
    email_notifier = EmailNotifier(
        smtp_server=os.getenv('SMTP_SERVER'),
        port=int(os.getenv('SMTP_PORT')),
        sender_email=os.getenv('EMAIL_USER'),
        sender_password=os.getenv('EMAIL_PASS'),
        recipient_email='juniorrincon1992@hotmail.com'
    )
    print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
    # Pasar el notificador de correos a menu_view
    menu_view(email_notifier)

if __name__ == "__main__":
    main()