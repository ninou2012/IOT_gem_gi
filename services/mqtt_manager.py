# Modèle d'intégration pour votre infrastructure IoT réelle
class MQTTManager:
    def __init__(self):
        self.client = None
        
    def start_listening(self):
        """Déclenche l'écoute des topics IoT en arrière-plan."""
        pass

    def on_message_received(self, client, userdata, msg):
        """
        À la réception d'un message IoT, on met directement à jour 
        le st.session_state.vehicles_data sans intermédiaire.
        """
        pass
