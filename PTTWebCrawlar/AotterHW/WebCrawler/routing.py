from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/WebCrawler/PythonUser/$', consumers.ChatConsumer),
    # url(r'^ws/WebCrawler/HTMLUser/$', consumers.ChatConsumerHTMLUser),
]
