from django.db import models
import pymongo

# 獲得 PTT 所有版的名稱
def GetAllBoardFromMongodb():
    # 從mongodb伺服器獲得 PTT 所有版的名稱
    # return list 所有有紀錄的PPT版名稱
    # 若有資料則回傳所有討論版名稱
    # 若無 (代表mongodb沒檔案 或是伺服器有問題) 則回傳 []
    AllBoard = pymongo.MongoClient('mongodb://root:123456@mongodbcontainer/')["PTTDataBase"]["AllBoard"].find_one()
    if AllBoard:
        return AllBoard['Data']
    else:
        return []
