from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add("payment_notify", self.channel_name)
		# print(f"Added {self.channel_name} channel to task")
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard("payment_notify", self.channel_name)
		# print(f"Removed {self.channel_name} channel to task")

	async def user_notification(self, event):
		await self.send_json(event)
		# print(f"Got message {event} at {self.channel_name}")