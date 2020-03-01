from django.conf.urls import url
from . import views
from . import consumers

'''
設定 API
1. test/   測試 Django 正常與否API
2. GetOneBoardName/ 傳送單個討論版名稱給使用者
'''
urlpatterns = [
    url(r'test/', views.test),
    url(r'GetOneBoardName/', views.ResponesOneBoardNameToUser),
    url(r'CheckHTML/', views.CheckHTML),
    url(r'GetNowAllWebCrawler/', consumers.GetNowAllWebCrawler),
]
