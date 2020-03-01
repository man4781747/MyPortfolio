# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:23:57 2020

@author: man47
"""
#%%
from bs4 import BeautifulSoup
import requests
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from websocket import create_connection
global S_monddbIP
global S_DjangoServerIp
import pymongo
import datetime

# 給出 我已滿18 用
Iam18Payload = {
            'from' : '/bbs/Gossiping/index.html',
            'yes' : 'yes'
        }

MonthSwitch = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def GetOneBoardNameFromServer():
    #從伺服器GET分發的PTT版名稱
    #return string 單個PTT版名稱
    
    
    GetBoardName = json.loads(requests.get(r'http://{0}/WedCrawler/GetOneBoardName/'.format(S_DjangoServerIp)).text)['BoardName']
    if GetBoardName == 'ALLPOST':
        # ALLPOST 版全都是 404 ERROR
        GetBoardName = json.loads(requests.get(r'http://{0}/WedCrawler/GetOneBoardName/'.format(S_DjangoServerIp)).text)['BoardName']
    
    return GetBoardName

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

def url2aid(S_url):
    # 將網址轉換為 AID
    # Input:  String PTT網址  範例: 'M.1557532946.A.A91.html'
    # Output: String AID "ABCEDFG" 共8個字符
    try:
        # Base64 的排序內容及順序
        Base = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
        
        # 將 S_url 以字符 '.' 分段
        List_Url = S_url.split('.')[:4]
        
        # 判斷第一字符是'M'還是'A'
        if List_Url[0] == 'M':
            S_1 = '0000'
        else:
            S_1 = '0001'
        
        Str_1 = List_Url[1]
        Str_2 = List_Url[3]
        # 有些較舊的網址沒有第四部分的16進位字符 所以將之判定為 000
        if Str_2 == 'html':
            Str_2 = '000'
            
        # 將第2部分10進位數字轉換為 bit形式並補滿長度為 32 (32 bit)
        Str_1_ToBin = bin(int(Str_1))[2:].zfill(32)
        # 將第2部分16進位文字轉換為 bit形式並補滿長度為 12 (12 bit)
        Str_2_ToBin = bin(int(Str_2,16))[2:].zfill(12)
        # 將所有部分合併為 32+12+4=48 bit
        Str_all = S_1+Str_1_ToBin+Str_2_ToBin
        # 48bit中 每 6bit 可轉為1個 base64 文字
        aid = ''
        for i in range(8):
            aid += Base[int('0b{0}'.format(Str_all[i*6:(i+1)*6]),2)]
        return aid
    except:
        print('ERROR!!!! in  {0}'.format(S_url))
        return False
    

def ReSearchAllRTTBoard():
    # 此為遍歷所有PTT的板的名稱
    # 功能為找到所有PTT各版的名稱
    
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
    AllBoardHTMLStack = []
    
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
                    AllBoardHTMLStack.append(URLGet)
                    # 分離出討論版名稱
                    S_BoardName = URLGet.split('/')[-2]
                    print('Find a board : {0}'.format(S_BoardName))
                    
                    # 若此版沒存在在mongodb紀錄中 則將其加入
                    if S_BoardName not in ExistAllBoardName:
                        ExistAllBoardName.append(S_BoardName)
                        myclient = pymongo.MongoClient(S_monddbIP)
                        mydb = myclient["PTTDataBase"]
                        mycol = mydb["AllBoard"]
                        mycol.delete_one({'name' :'AllBoardList'})
                        mycol.insert_one({"name" :"AllBoardList" , 'Data': ExistAllBoardName})       
        time.sleep(0.1)

def SearchSingleRTTBoard(S_BoardName,TimeUpperBound,TimeLowerBound,test=False):
    # 找尋單個版的所有文章的
    # 找查單一各版所有頁面的文章 並爬出所需內容
    # Input:
    #   S_BoardName : string 討論版名稱
    #   TimeUpperBound : datetime.datetime 選取時間範圍上界
    #   TimeLowerBound : datetime.datetime 選取時間範圍下界
    try:
        # PTT文章網址基本長相
        PttUrlPath = r'https://www.ptt.cc/bbs/{0}/index{1}.html'
        
        # 先GET當前討論版的首頁內容
        rs = requests.session()
        r = rs.post(r'https://www.ptt.cc/ask/over18',verify=False, data=Iam18Payload)
        r = rs.get(PttUrlPath.format(S_BoardName,''),verify=False).content
        # 避免爬得太快被BAN
        time.sleep(0.1)
        
        # 抓取藥的主要內容的部分 id 為 'main-container'
        MainContent = BeautifulSoup(r, 'lxml').find(id='main-container')
    
        # 去檢查有沒有 '上頁' 的按鈕 若有則可抓取此版所有的頁數
        # 若沒有 則代表頁數只有 1
        ButtonAll = MainContent.find_all('div',class_='btn-group btn-group-paging')[0].find_all()
        if len(ButtonAll[1].get('class')) == 2:
            if test:
                # 若為測試模式 只抓取第一頁
                print('Test Mode!!')
                AllPageNum = 1
            else:
                AllPageNum = int(ButtonAll[1].get('href').split('/')[-1][5:-5])+1
        else:
            AllPageNum = 1
            
        print('Now IN Board: {0} it have {1} Page'.format(S_BoardName, AllPageNum))
        
        # 與 mongodb 連線 並去搜尋當前紀錄中以存在的 AID
        # 若存在 則代表此篇文章已被爬過了
#        myclient = pymongo.MongoClient(S_monddbIP)
#        mydb = myclient["PTTDataBase"]
#        mycol = mydb["AllData"]
#        L_AlreadyExists = mycol.find(
#                    {"ArticleCategory": "{0}".format(S_BoardName)}, {"aid":1}
#                )
#        L_AlreadyExists = [AIDExists['aid'] for AIDExists in L_AlreadyExists]
        
        # 給出我已滿18
        rs_PageChose = requests.session()
        r_PageChose = rs_PageChose.post(r'https://www.ptt.cc/ask/over18',verify=False, data=Iam18Payload)
        
        # 開始遍歷每頁內容
        SearchType = 0
        NowChosePageNum = 1
        while NowChosePageNum <= AllPageNum:
            
            # 傳送 WebSocket 訊息 更新此爬蟲程式搜索頁面
            ws.send('NewPage\n{0}'.format(NowChosePageNum))
#        for i in range(AllPageNum,0,-1):
            print('Now In Page: {0}'.format(PttUrlPath.format(S_BoardName,NowChosePageNum)))
            
            
            # 抓去討論版當前頁數的內容 並抓出所需要物件 id='main-container'
            r_PageChose = rs_PageChose.get(PttUrlPath.format(S_BoardName,NowChosePageNum)).content
            MainContent_PageChose = BeautifulSoup(r_PageChose, 'lxml').find(id='main-container')
            
            # 所有標題跟連結都在 'div',class_='title' 中
            UrlsGet = MainContent_PageChose.find_all('div',class_='title')
            time.sleep(0.1)
            
            if SearchType == 0:
                print('SearchType = 0')
                # 第一順位找尋文章方法
                # 目的為快速判斷此頁到底有沒有機會有文章在時間範圍內
                # 找尋最舊頁面最後一篇文章 若發現最後一篇文章(當前頁面最新的文章) 的發文時間比
                # 設定的時間區間下界還舊 代表整篇文章都不可能有時間範圍內文章 
                # 則直接跳轉至下一頁 並繼續比較最後一篇文章(當前頁面最新的文章)時間
                # 直到發現開始有文章的時間比設定的時間區間下界還新 則將 SearchType 更改為 1
                
                # 若處於 SearchType == 0 但 NowChosePageNum == AllPageNum
                # 則代表在最新頁面且尚未找到符合大於下界範圍的文章
                # 此時因為有至頂文章的問題 所以不能查看最下方文章的時間當作時間標準
                # 因此直接轉為  SearchType = 1
                # 反正也沒有後續頁面了 不需要用 SearchType = 0 的方法去快速篩選頁面
                
                if NowChosePageNum != AllPageNum:
                    for Chose_URL_ in UrlsGet[::-1]:
                        #找尋當前頁面文章(由新到舊)
                        Get_URL_ = Chose_URL_.find_all('a')[0].get('href')
                        PageInfo = GetPageInfo(r'https://www.ptt.cc{0}'.format(Get_URL_))
    #                    print(PageInfo)
                        # 若 PageInfo 值正常則代表解析正常 若值為None則代表爬蟲沒抓正常
                        # 若 PageInfo 為None 代表抓不到時間無法確定貼文時間 則開始找下一篇文章的時間
                        # 迴圈到底如果都抓不到時間 則當作整頁都沒時間 
                        if PageInfo:
                            DateTimeInfo = PageInfo[4].split(' ')
                            TimeInfo = DateTimeInfo[-2].split(':')
                            PostingDateTime = datetime.datetime(
                                        int(DateTimeInfo[-1]),
                                        MonthSwitch.index(DateTimeInfo[1]),
                                        int(DateTimeInfo[-3]),
                                        int(TimeInfo[0]),
                                        int(TimeInfo[1]),
                                        int(TimeInfo[2])
                                    )
                            # 如果發現該文章貼文時間比設定時間下界還大 則代表其可能在範圍內
                            # 將 SearchType 更改為1
                            # 並跳脫出 FOR 迴圈
                            # 若 發現該文章貼文時間比設定時間下界還小 則代表此頁不可能有時間範圍內文章
                            # 將 NowChosePageNum 加上 1 
                            # 並跳脫出 FOR 迴圈 直接去搜尋下一頁頁面
                            
                            if PostingDateTime >= TimeLowerBound:
                                SearchType = 1
                                NowChosePageNum -= 1
                                break
                            else:
                                print('Page {0} dont have new enough articles'.format(r'https://www.ptt.cc{0}'.format(Get_URL_)))
                                break
                else:
                    SearchType = 1
                    NowChosePageNum -= 1
                # 若整篇都沒時間 NowChosePageNum += 1
                NowChosePageNum += 1
            elif SearchType == 1:
                print('SearchType = 1')
                # 第二類找尋文章方法
                # 代表當前頁面可能有時間範圍內文章
                # 開始從當前頁面第一篇文章(最舊)開始找起
                
                # 若頁面不是最新頁(沒有至頂文問題)
                for Chose_URL_ in UrlsGet:
                    #找尋當前頁面文章(由舊到新)
                    Get_URL_ = Chose_URL_.find_all('a')[0].get('href')
                    PageInfo = GetPageInfo(r'https://www.ptt.cc{0}'.format(Get_URL_))
                    # 若 PageInfo 值正常則代表解析正常 若值為None則代表爬蟲沒抓正常
                    # 若 PageInfo 為None 代表抓不到時間無法確定貼文時間 則開始找下一篇文章的時間
                    if PageInfo:
                        DateTimeInfo = PageInfo[4].split(' ')
                        TimeInfo = DateTimeInfo[-2].split(':')
                        PostingDateTime = datetime.datetime(
                                    int(DateTimeInfo[-1]),
                                    MonthSwitch.index(DateTimeInfo[1]),
                                    int(DateTimeInfo[-3]),
                                    int(TimeInfo[0]),
                                    int(TimeInfo[1]),
                                    int(TimeInfo[2])
                                )
                        # 如果發現該文章貼文時間比設定時間上界還大 則代表整個討論版沒有符合範圍的文章
                        # 因為更小數字頁面沒有比時間下界更新的文章
                        # 又往後頁樹文章沒有比時間上界更舊的文章
                        # 如果發現該文章貼文時間比設定時間上界還小 
                        # 將 NowChosePageNum 更改為 AllPageNum 並跳脫迴圈
                        # 則代表此文章在範圍內 可爬
                        if PostingDateTime <= TimeUpperBound:
                            if PostingDateTime >= TimeLowerBound:
                                # 此文章在範圍內
                                myclient = pymongo.MongoClient(S_monddbIP)
                                mydb = myclient["PTTDataBase"]
                                mycol = mydb["AllData"]
                                aidGet = url2aid(Get_URL_)
                                NowTime = time.time()
                                # 查看文章是否已有紀錄
                                try:
                                    IfExist = mycol.find({'ArticleCategory':S_BoardName,'aid':'{0}'.format(aidGet)})[0]
                                except:
                                    IfExist = None
                                # 若此篇文章已有紀錄 則更新內容(除了createdTime之外其餘全部更新)
                                if IfExist:
                                    mycol.update({
                                                "ArticleCategory" : PageInfo[3] ,
                                                'aid': aidGet,
                                            },{
                                                    "ArticleCategory" : PageInfo[3] ,
                                                    'aid': aidGet,
                                                    'Title' : PageInfo[2],
                                                    'authorID' : PageInfo[1],
                                                    'authorName' : PageInfo[0],
                                                    'PostingTime' : PageInfo[4],
                                                    'canonicalUrl' : r"https://www.ptt.cc{0}".format(Get_URL_),
                                                    'content' : PageInfo[5],
                                                    'Pushs' : PageInfo[6],
                                                    'createdTime' : IfExist['createdTime'],
                                                    'updateTime' : NowTime
                                                }
                            )
                                # 若此篇文章沒有紀錄 則新增內容
                                else:
                                    mycol.insert_one(
                                            {
                                                    "ArticleCategory" : PageInfo[3] ,
                                                    'aid': aidGet,
                                                    'Title' : PageInfo[2],
                                                    'authorID' : PageInfo[1],
                                                    'authorName' : PageInfo[0],
                                                    'PostingTime' : PageInfo[4],
                                                    'canonicalUrl' : r"https://www.ptt.cc{0}".format(Get_URL_),
                                                    'content' : PageInfo[5],
                                                    'Pushs' : PageInfo[6],
                                                    'createdTime' : NowTime,
                                                    'updateTime' : NowTime
                                                    }
                                            )
                                
                                
                                
                                
                                print('Find!!!!')
                                print(PageInfo[2])
                                print(PostingDateTime)
                                print(r"https://www.ptt.cc{0}".format(Get_URL_))
                        else:
                            # 若文章時間已經比時間上界還大
                            # 代表往後文章都太新了
                            # 則將 NowChosePageNum 設定為 AllPageNum 
                            # 跳至最新頁查看是否有範圍內的至頂文
                            # 並 跳脫出FOR迴圈
                            print('Target article is no longer available in Board {0}'.format(S_BoardName))
                            NowChosePageNum = AllPageNum
                            break
                #  若for迴圈跑完了 則代表
                #    1. 整頁文章都看過了 並且沒超出範圍 或是 找不到時間
                #    2. 已經發現超出範圍了
                #  此時 NowChosePageNum += 1
                #  情況 1. 就會繼續蒐尋下一頁 (若頁面沒了就會跳脫 while )
                #  情況 2. 沒有範圍內文章了 跳脫 while
                
                NowChosePageNum += 1
                
    except Exception as e:
        print('Get Some Error in board {0}'.format(S_BoardName))
        print(e)
        return False
    return True

def SearchAllRTTBoard(test=False):
    # 自動搜尋所有版的所有頁面的所有文章內容
    # 備用用 不太會使用到
    if test:
        print('Test Mode!!')
    for S_BoardNameChose in GetAllBoardFromMongodb():
        SearchSingleRTTBoard(S_BoardNameChose, test)


def GetPageInfo(S_url):
    # 此系列程式核心 主要爬蟲內容
    # Input: string S_url 文章網頁  例如 'https://www.ptt.cc/bbs/FCK-HSING/M.1374506549.A.1F6.html'
    # Output: List [
    #       authorName,          string 作者暱稱
    #       authorID,            string 作者ID
    #       Title,               string 文章標題
    #       ArticleCategory,     string 文章分類
    #       PostingTime,         string 貼文時間
    #       MainContent,         string 文章內容
    #       PushSaveList         list 推文內容  [
    #                                            string  推文者ID,
    #                                            string  推文時間,
    #                                            string  推文類型,
    #                                            string  推文內容
    #                                          ]
    #   ]
    try:
        # post 我已滿18訊息 並獲得文章內所需要內容 id='main-content'
        rs = requests.session()
        r = rs.post(r'https://www.ptt.cc/ask/over18',verify=False, data=Iam18Payload)
        r = rs.get(S_url,verify=False).content
        MainContent = BeautifulSoup(r, 'lxml').find(id='main-content')
        
        # 獲得 'span',class_='article-meta-value' 的內容 
        # 其中包含了 作者編號 作者暱稱 標題 文章分類 貼文時間
        TitleInfo = MainContent.find_all('span',class_='article-meta-value')
        authorInfo = TitleInfo[0].get_text()
        authorName = authorInfo[authorInfo.find('(')+1:len(authorInfo)-1]
        authorID = authorInfo[:authorInfo.find('(')]
        Title = TitleInfo[2].get_text()
        ArticleCategory = TitleInfo[1].get_text()
        PostingTime = TitleInfo[3].get_text()
        
        # 將不需要的內容消去
        for TitleInfoChose in TitleInfo:
            TitleInfoChose.decompose()
        
        # 將所有推文的 推文IP+時間的刺串做處理 多加個 \t 在前方 方便後續處理
        for PushChose in MainContent.find_all('div',class_='push'):
            PushChoseIPDateTime = PushChose.find('span', class_='push-ipdatetime')
            PushChoseIPDateTime.string = '\t' + PushChoseIPDateTime.get_text()
        
        # 單獨取出 本文內容及推文部分
        AfterTitle = MainContent.get_text()[9:]
        
        # 用'※ 發信站'分離出 MainContent 主要文章內容
        MainContent = AfterTitle[:AfterTitle.find('※ 發信站')]
        # 用'※ 發信站'分離出 所有推文內容 並以 '\n' 分類
        AllPush = AfterTitle[AfterTitle.find('※ 發信站'):].split('\n')
        
        # AllPush 推人內容會是以 string方式 例如 '推 pusherID: 推文內容 \t127.0.0.1 02/02 20:34'
        PushSaveList = []
        for PushChose in AllPush:
            # 防止什麼都沒有的單行
            if len(PushChose) > 0:
                # 去除非推文的行數
                if PushChose[0] in ['噓' , '推' , '→']:
                    # 推文者ID位置在 PushChose[2:PushChose.find(':')]
                    PusherId = PushChose[2:PushChose.find(':')]
                    # 推文時間位置在 PushChose[len(PushChose)-11:]
                    PushDateTime = PushChose[len(PushChose)-11:]
                    # 推文內容位置在 PushChose[PushChose.find(':')+1:len(PushChose)-12].split('\t')[0][1:]
                    # 前方預先對字串作處理就是用在這 因為有發現貼文內容跟IP黏在一起的問題
                    PushComtant = PushChose[PushChose.find(':')+1:len(PushChose)-12].split('\t')[0][1:]
                    PushSaveList.append([PusherId,PushDateTime,PushChose[0],PushComtant])
        return [authorName, authorID, Title, ArticleCategory, PostingTime, MainContent, PushSaveList]
    
    except Exception as e:
        # 若爬文過程中出錯 則將訊息紀錄至 mongodb
        myclient = pymongo.MongoClient(S_monddbIP)
        mydb = myclient["PTTDataBase"]
        mycol = mydb["GetErrorUrl"]
        info = {
                    'Url' : S_url ,
                    'ErrorInfo' : str(e) , 
                    'ErrorTime' : time.time()
                }
        mycol.insert_one(info)
        print('Function GetPageInfo Get Error : {0}'.format(e))    
        return None
    
    
    
def AutoSingleBoardGet(DateTimeUpper,DateTimeLow, test = False):
    # 主要功能 跟伺服器要討論版名稱 並爬蟲 完整爬完後會再繼續下一個迴圈
    while 1:
        GetBoardName = GetOneBoardNameFromServer()
        if GetBoardName:
            # 傳送 WebSocket 訊息 更新此爬蟲程式搜索的看板
            print('==================')
            print('Search Infomation:')
            print('WebCrawlerName: {0}\nSearchedBoardName: {1}\nUpperTime: {2}\nlowerTime: {3}'.format(S_WebSocketName,GetBoardName,DateTimeUpper,DateTimeLow))
            print('==================')
            ws.send('NewBoard\n{0}\n{1}\n{2}\n{3}'.format(S_WebSocketName,GetBoardName,DateTimeUpper,DateTimeLow))
            SearchSingleRTTBoard(GetBoardName,DateTimeUpper,DateTimeLow, test)
        else:
            print('Cant Get BoardName From Server!!!')
            break
    
if __name__ == '__main__':
    L_ConfigRead = open(r'./config.txt').read().split('\n')
    S_WebSocketName = L_ConfigRead[4][14:].strip()
    B_TestMode = False
    # S_monddbIP: mongodb 的IP位置
    S_monddbIP = 'mongodb://root:123456@{0}:27000'.format(L_ConfigRead[0][9:].strip())
    # S_DjangoServerIp: DjangoServer 的IP位置
    S_DjangoServerIp = '{0}:8001'.format(L_ConfigRead[0][9:].strip())
    DateTimeUpper = datetime.datetime.strptime(
                L_ConfigRead[1][10:].strip(), 
                "%Y-%m-%d %H:%M:%S"
            )
    DateTimeLow = datetime.datetime.strptime(
                L_ConfigRead[2][10:].strip(), 
                "%Y-%m-%d %H:%M:%S"
            )
    # 與 Server Websockit 連線
    ws = create_connection("ws://{0}:8001/ws/WebCrawler/PythonUser/".format(L_ConfigRead[0][9:].strip()))
    
    
    # 檢查是否已有正確的 PTT所有板名稱紀錄
    myclient = pymongo.MongoClient(S_monddbIP)
    if not GetAllBoardFromMongodb():
        print('bomgodb dont have AllBoard Data!!!!!!!')
        ReSearchAllRTTBoard()
        
        print('OK!!!')
    
    AutoSingleBoardGet(DateTimeUpper,DateTimeLow,test=B_TestMode)
    