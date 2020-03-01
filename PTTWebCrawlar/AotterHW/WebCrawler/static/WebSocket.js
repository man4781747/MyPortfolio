/*
此程式負責接收伺服器 WebSocket 的廣播時的反應
*/
// var chatSocket = new WebSocket('ws://' + window.location.host +'/ws/WebCrawler/PythonUser');
var chatSocket = new WebSocket('ws://' + window.location.host +'/ws/WebCrawler/HTMLUser/');
// 接收廣播
chatSocket.onmessage = function(e) {
    console.log('從伺服器收到廣播');
    var data = JSON.parse(e.data)['message'];
    console.log(data)



    // var data = JSON.parse(e.data);
    // var message = JSON.parse(e.data)['message'];
    // if (message['DataType'] == 'AddNewData' & AllStationData.length!=0){
    //   // 當收到的廣播的 DataType 為 AddNewData
    //   // 觸發 DataProcessing.js 中的 UpdateData()
    //   UpdateData(message);
    //   // console.log('AddNewData');
    // } else if (message['DataType'] == 'ChangeData') {
    //   // 當收到的廣播的 DataType 為 ChangeData
    //   // 觸發 DataProcessing.js 中的 WhenGetAllData()
    //   WhenGetAllData(message);
    // } else {
    //   console.log('testttt')
    // }
    // // console.log(message);
};
