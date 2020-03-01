# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 09:31:14 2020

@author: man47

此程式為更新爬蟲在mongodb紀錄的PTT討論版名稱內容
"""

from bs4 import BeautifulSoup
import requests
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import pymongo

# 給出 我已滿18 用
Iam18Payload = {
            'from' : '/bbs/Gossiping/index.html',
            'yes' : 'yes'
        }

def GetAllBoardFromMongodb():
    # 從mongodb伺服器獲得 PTT 所有版的名稱
    # return list 所有有紀錄的PPT版名稱
    # 若有資料則回傳所有討論版名稱
    # 若無 (代表mongodb沒檔案 或是伺服器有問題) 則回傳 []
    AllBoard = pymongo.MongoClient(S_monddbIP)["PTTDataBase"]["AllBoard"].find_one()
    if AllBoard:
        return AllBoard['Data']
    else:
        return []

def ReSearchAllRTTBoard():
    # 此為遍歷所有PTT的板的名稱
    # 功能為找到所有PTT各版的名稱
    myclient = pymongo.MongoClient(S_monddbIP)
    mydb = myclient["PTTDataBase"]
    mycol = mydb["AllBoard"]
    
    
    # post 我已18內容 並先找查 PTT 的分類看板
    rs = requests.session()
    r = rs.post(r'https://www.ptt.cc/ask/over18',verify=False, data=Iam18Payload)
    r = rs.get(r'https://www.ptt.cc/cls/1',verify=False).content
    
    # 需要內容都再 id='main-container' 物件內
    MainContent = BeautifulSoup(r, 'lxml').find(id='main-container')
    
    # AllBoardStack 待查的URL
    AllBoardStack = []
    # 防止重複搜查版
    AllBoardSave = []
    # 目前擁有的討論版名稱
    ExistAllBoardName = GetAllBoardFromMongodb()
    
    # 先將分類看板下的所有連結存入 stack內待查
    for BoardUrlChose in MainContent.find_all('a',class_='board'):
        AllBoardStack.append(BoardUrlChose.get('href'))
        
    rsNow = requests.session()
    # 若stack內尚存待查URL
    while AllBoardStack:
        print('Still have {0} URL'.format(len(AllBoardStack)))
        # pop 出待查URL
        PttUrlPathChose = r'https://www.ptt.cc' + AllBoardStack.pop()
        
        # post 我已18內容 並先找查頁面下所有連結
        rNow = rsNow.post(r'https://www.ptt.cc/ask/over18',verify=False, data=Iam18Payload)
        rNow = rs.get(PttUrlPathChose,verify=False).content
        NowMainContent = BeautifulSoup(rNow, 'lxml').find(id='main-container')
        
        # BoardUrlChose 為單個連結內容
        for BoardUrlChose in NowMainContent.find_all('a',class_='board'):
            # URLGet 分離出的網址
            URLGet = BoardUrlChose.get('href')
            
            if URLGet[0] == '/':
                # 如果網址最後部分為 'html' 則代表找到一個討論版了
                # 反之 若不是 則代表還有後續路徑
                if URLGet[-4:] != 'html':
                    # 若還有後續路徑
                    # 抓出後續路徑 網址數字部分
                    URLNum = int(URLGet.split('/')[-1])
                    # 若此網址在此次搜查中沒被查過的話
                    if URLNum not in AllBoardSave:
                        # 紀錄以來當作查過了
                        AllBoardSave.append(URLGet)
                        # 放入待查
                        AllBoardStack.append(URLGet)
                else:
                    # 若判斷為討論版了
                    
                    # 分離出討論版名稱
                    S_BoardName = URLGet.split('/')[-2]
                    print('Find a board : {0}'.format(S_BoardName))
                    
                    # 若此版沒存在在mongodb紀錄中 則將其加入
                    if S_BoardName not in ExistAllBoardName:
                        print('ADD New Board : {0}'.format(S_BoardName))
                        ExistAllBoardName.append(S_BoardName)
                        mycol.delete_one({'name' :'AllBoardList'})
                        mycol.insert_one({"name" :"AllBoardList" , 'Data': ExistAllBoardName})  
                    else:
                        print('Board : {0} Exist!!'.format(S_BoardName))
        time.sleep(0.1)
        
if __name__ == '__main__':
    L_ConfigRead = open(r'./config.txt').read().split('\n')
    # S_monddbIP: mongodb 的IP位置
    S_monddbIP = 'mongodb://root:123456@{0}:27000'.format(L_ConfigRead[0][9:].strip())
    ReSearchAllRTTBoard()