import streamlit as st
from notifiers.email_notifier import EmailNotifier
from views.welcome_view import show_welcome
from views.menu_view import menu_view
from views.data_management_view import run_gui
from views.home_view import home_view
from config import config
from dotenv import load_dotenv
import os

config.setup_app()
load_dotenv()


print("Usuario:", os.getenv('EMAIL_USER'))
print("Contraseña:", os.getenv('EMAIL_PASS'))

def main():
    st.title("Alert System Dashboard")
    
    # Configurar el notificador de correos
    emailnotifier = EmailNotifier(
    smtp_server=os.getenv('SMTP_SERVER'),
    port=int(os.getenv('SMTP_PORT')),
    sender_email=os.getenv('EMAIL_USER'),
    sender_password=os.getenv('EMAIL_PASS'),
    recipient_email='juniorrincon1992@hotmail.com'
    )
    
    menu_view()
    


if __name__ == "__main__":
    main()
