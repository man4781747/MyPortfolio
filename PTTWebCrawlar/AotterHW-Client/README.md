此程式功能為爬蟲主要程式 一個伺服器可以搭配多個客戶端
====

可使用docker 執行或是直接用python(3.7)執行
所需套件紀錄於 requirements.txt


執行前 請先至 config.txt 中更改各項設定
  ServerIP: 伺服器IP位置
  UpperTime: 搜尋文章的時間區間上界
  LowerTime:  搜尋文章的時間區間下界
  TestMode: 使否用測試模式
  WebSocketName: 替此庫戶端命名 此名稱可在  " "IP網址":8081/WedCrawler/GetNowAllWebCrawler/ "  中看到
                 方便用戶追蹤

架設方法
cd 至該資料夾下後 輸入: 

docker-compose up

即可

或執行 python RunThis.py
