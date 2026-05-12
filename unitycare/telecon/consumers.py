from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs


class TeleconConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket signaling + chat consumer for WebRTC rooms.
    - Clients join a room via URL path: ws://.../ws/telecon/<room_name>/?role=doctor|patient
    - Messages are JSON with a required 'type' field.
      Supported types:
        - 'chat': {message}
        - 'offer': {sdp}
        - 'answer': {sdp}
        - 'candidate': {candidate}
        - 'presence': {status}
    """

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"telecon_{self.room_name}"

        # Optional role query param (doctor/patient)
        query = parse_qs(self.scope.get("query_string", b"").decode())
        self.role = (query.get("role", ["guest"]))[0]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify presence
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast",
                "payload": {
                    "type": "presence",
                    "status": "joined",
                    "role": self.role,
                },
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Notify presence
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast",
                "payload": {
                    "type": "presence",
                    "status": "left",
                    "role": self.role,
                },
            },
        )

    async def receive_json(self, content, **kwargs):
        # Relay incoming messages to the whole room
        msg_type = content.get("type")
        if msg_type in {"chat", "offer", "answer", "candidate", "presence"}:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "payload": content,
                },
            )
        else:
            # Unknown type ignored
            pass

    async def broadcast(self, event):
        await self.send_json(event["payload"])