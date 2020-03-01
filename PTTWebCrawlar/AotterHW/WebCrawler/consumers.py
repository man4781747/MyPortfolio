from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.layers import get_channel_layer
from django.http import JsonResponse
global NowAllWebCrawler
NowAllWebCrawler = {}
from django.views.decorators.csrf import csrf_exempt
from . import views


@csrf_exempt
def GetNowAllWebCrawler(request):
    return JsonResponse(NowAllWebCrawler)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'TestGroup'
        print('有人連近來拉 : '.format(self.channel_name))
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        disconnectInfo = NowAllWebCrawler.pop(self.channel_name)['GetBoardName']
        views.AllBoardNameADD(disconnectInfo)
        print('有人斷線拉 : {0}'.format(self.channel_name))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )



    # Receive message from WebSocket
    def receive(self, text_data):
        TextSplit = text_data.split('\n')
        if TextSplit[0] == 'NewBoard':
            NowAllWebCrawler[self.channel_name] = {
                'WebCrawlerName' : TextSplit[1],
                'GetBoardName' : TextSplit[2],
                'DateTimeUpper' : TextSplit[3],
                'DateTimeLow' : TextSplit[4]
            }

        if TextSplit[0] == 'NewPage':
            NowAllWebCrawler[self.channel_name]['NowPage'] = TextSplit[1]



# class ChatConsumerHTMLUser(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'HTMLUser'
#         print('有人連近來拉 : '.format(self.channel_name))
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         print('有人斷線拉 : '.format(self.channel_name))
#
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         print('=======================')
#         channel_layer = get_channel_layer()
#
#         channel_layer.group_send(
#             'HTMLUser',
#             {
#                 "type": "chat_message",
#                 'message' : {'test':'test'}
#             }
#         )
#
#         # async_to_sync(channel_layer.group_send)(
#         #     'HTMLUser',
#         #     {
#         #         "type": "chat_message",
#         #         'message' : {'test':'test'}
#         #     }
#         # )
#         print('---------------------')
#
#     # Receive message from room group
#     def chat_message(self, event):
#         pass
