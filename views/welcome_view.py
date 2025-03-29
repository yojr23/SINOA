from utils.transitions_utils import transitions


def show_welcome():
    """Muestra solo la animación de bienvenida"""
    transitions.welcome_animation()

if __name__ == "__main__":
    show_welcome()