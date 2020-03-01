from django.shortcuts import render
from django.http import JsonResponse
import os
from . import models

# 獲得 mongodb中紀錄的已有的所有討論版名稱
global AllBoardName
AllBoardName = models.GetAllBoardFromMongodb()

def AllBoardNameADD(S_BoardName):
    print('Board {0} Search Interrupted !!!!!'.format(S_BoardName))
    AllBoardName.append(S_BoardName)

def CheckHTML(request):
    return render(request, 'WebCrawlerCheck.html', {})

# 測試用
def test(request):
    return JsonResponse({'AllPicDate':[1,2,3]})

# 傳送單個討論版名稱給使用者
def ResponesOneBoardNameToUser(request):
    global AllBoardName
    # 若發現已經分發完名稱一輪了 則從新獲取名單
    if len(AllBoardName) == 0:
        AllBoardName = models.GetAllBoardFromMongodb()
    try:
        return JsonResponse({'BoardName' : AllBoardName.pop()})
    except:
        # 若名單已經空了(不正常) 則回傳None
        return JsonResponse({'BoardName' : None})
