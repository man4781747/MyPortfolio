'''
此為 channels 的設定
'''

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import WebCrawler.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            WebCrawler.routing.websocket_urlpatterns
        )
    ),

})
