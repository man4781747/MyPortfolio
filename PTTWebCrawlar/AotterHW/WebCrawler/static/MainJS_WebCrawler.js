
var AllStationData;


function setup() {
  AllStationData = [];

  chatSocket.send(JSON.stringify({
      'message': {
        'MessageType':'GiveUpMessage'
                }
  }));
/*
  開啟網頁後 第一步就對伺服器傳送websock的請求
  格式
  'message': {
    'StationName': 要求資料的站名,
    'DataLen':     要求的資料長度最大值
            }

  在 WebSocket.js 中設定網頁接收伺服器的 WebSocket 廣播反應
*/

  // createCanvas(windowWidth, windowHeight);
  // setTimeout(function(){
  //   for (let i = 0;i<StationInfo.length;i++){
  //     chatSocket.send(JSON.stringify({
  //         'message': {'StationName':StationInfo[i].name,
  //                     'DataLen':DataLenMax[i]}
  //     }));
  //   }
  //  }, 1000);

  // setTimeout(function(){ MainWindow(); }, 1000);
}

// function draw() {
//   console.log('test')
// }
