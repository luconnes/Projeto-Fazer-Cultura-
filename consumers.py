import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Aceita a conexão WebSocket

        # Envia uma mensagem ao cliente com a confirmação de conexão
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected!'
        }))
