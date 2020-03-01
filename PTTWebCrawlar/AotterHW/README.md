此程式為PTT爬蟲程式伺服器端
====

此伺服器用 Django 架設 
使用了 redis與channels 搭配來監控爬蟲端狀態
使用了 mongodb 來儲存資料

其使用到之 python 套件紀錄於 requirements.txt

使用 docker 來架設

架設方法

cd 至該資料夾下後 輸入:
    docker-compose up 
即可

看到下列圖片後的內容代表成功

![](https://github.com/man4781747/MyPortfolio/blob/master/PTTWebCrawlar/AotterHW/ExapmlePic/Check2.PNG)
![](https://github.com/man4781747/MyPortfolio/blob/master/PTTWebCrawlar/AotterHW/ExapmlePic/Check1.PNG)

此時瀏覽網址( IP 可為 127.0.0.1 或該電腦IP ) 
1. "IP網址":8001/WedCrawler/test/    例如: 127.0.0.1:8001/WedCrawler/test/
      可看到測試網頁(以下畫面為 FireFox 瀏覽器畫面)

![](https://github.com/man4781747/MyPortfolio/blob/master/PTTWebCrawlar/AotterHW/ExapmlePic/TestExample.PNG)

2. "IP網址":8081                    例如: 127.0.0.1:8081/
      可看到 mongodb 的網頁視覺化呈現
       PTTDataBase 下為各資料的儲存
       (1) AllBoard     為紀錄的所有PTT討論版名稱
       (2) AllData      為爬蟲的結果
       (3) GetErrorUrl  為爬蟲錯誤的網址以及錯誤內容
       ## 若沒看到各分支 則代表還沒爬到相關資料
![](https://github.com/man4781747/MyPortfolio/blob/master/PTTWebCrawlar/AotterHW/ExapmlePic/mongodb%20Express%20Example.PNG)

3. "IP網址":8081/WedCrawler/GetNowAllWebCrawler/      例如: 127.0.0.1:8081/WedCrawler/GetNowAllWebCrawler/
      可看到目前連線的爬蟲程式以及其狀態

![](https://github.com/man4781747/MyPortfolio/blob/master/PTTWebCrawlar/AotterHW/ExapmlePic/GetNowAllWebCrawler.PNG)
