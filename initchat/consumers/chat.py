from channels.generic.websocket import AsyncWebsocketConsumer
from json import (
    loads,
    dumps
)
from minions import (
    generate_ai_response
)

class Chat(AsyncWebsocketConsumer):
    async def connect(self):
        # self.group_name = 'aichat'
        # await self.channel_layer.group_add(
        #     self.group_name,
        #     self.channel_name
        # )

        return await self.accept()

    async def disconnect(self, *args):
        # return await self.channel_layer.group_discard(
        #     self.group_name,
        #     self.channel_name
        # )

        pass
    
    async def receive(self, text_data=None, bytes_data=None):
        data = loads(text_data) if text_data else {}
        message = data.get('message', '')
        event = {
            'type': 'send_message',
            'message': message,
            'from': 'user'
        }

        # return await self.channel_layer.group_send(
        #     self.group_name,
        #     event
        # )

        await self.send(
            text_data=dumps(event)
        )

        if message:
            ai_response = generate_ai_response(message)
            data['from'], data['message'] = 'ai', ai_response
            await self.send(
                text_data=dumps(data)
            )

        return
    
    # async def send_message(self, data={}):
    #     message = data.get('message')
    #     await self.send(
    #         text_data=dumps(data)
    #     )

    #     if message:
    #         ai_response = generate_ai_response(message)
    #         data['from'], data['message'] = 'ai', ai_response
    #         await self.send(
    #             text_data=dumps(data)
    #         )

    #     return