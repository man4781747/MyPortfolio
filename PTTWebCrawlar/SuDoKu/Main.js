var MainBoard;
var L_Box;
var L_BigRow,L_BoxGroup;
var SetValueWindow;
var LestClick_x,LestClick_y;
var BaseWindow;
var SimBoard;
var CanChange_List;
var BoardInput;
function setup() {
  BaseWindow = null;
  noCanvas();
  var board = [
    [".",".","9","7","4","8",".",".","."],
    ["7",".",".",".",".",".",".",".","."],
    [".","2",".","1",".","9",".",".","."],
    [".",".","7",".",".",".","2","4","."],
    [".","6","4",".","1",".","5","9","."],
    [".","9","8",".",".",".","3",".","."],
    [".",".",".","8",".","3",".","2","."],
    [".",".",".",".",".",".",".",".","6"],
    [".",".",".","2","7","5","9",".","."]]

  var board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]]

  BuildNewGame();
}

function BuildNewGame(){
  var request = new XMLHttpRequest();
  request.open('get', 'http://allsky-airglow.earth.ncku.edu.tw/MiscModel/GetNewSudoku', false);
  request.send();
  BoardInput = JSON.parse(request.response)['NewBoard'];
  CanChange_List = [];
  if (BaseWindow){
    BaseWindow.remove()
  }
  SimBoard = new BoardSet_Sim(BoardInput);
  BaseWindow = createDiv();

  let NewGameBut = createButton("New Game");
  NewGameBut.parent(BaseWindow);
  NewGameBut.mouseClicked(x => {BuildNewGame()})
  let AnsBut = createButton("Ans");
  AnsBut.parent(BaseWindow);
  AnsBut.mouseClicked(x => {GetAns()})

  MainBoard = createDiv();
  MainBoard.parent(BaseWindow);
  // let TestDiv = createButton('test');
  // TestDiv.id('TestDiv')
  // TestDiv.parent(BaseWindow);
  // MainBoard.size(900+2.5, 900+2.5);
  MainBoard.id('MainBoardDiv')
  L_Box = [];
  for (let i=0;i<9;i++){
    L_Box.push([]);
    for (let j=0;j<9;j++){
      L_Box[i].push(null)
    }
  }

  L_BigRow = [];
  L_BoxGroup = [];
  for (let i=0;i<3;i++){
    let BigRowDiv = createDiv();
    BigRowDiv.class('BigRowDiv');
    BigRowDiv.parent(MainBoard);
    L_BigRow.push(BigRowDiv);
    for (let j=0;j<3;j++){
      let BigColDiv = createDiv();
      BigColDiv.class('BigColDiv');
      BigColDiv.parent(BigRowDiv);
      L_BoxGroup.push(BigColDiv);
      for (let k=0;k<3;k++){
        let SmallRow = createDiv();
        SmallRow.class('SmallRow');
        SmallRow.parent(BigColDiv);
        for (let l=0;l<3;l++){

          let BoxDiv = createDiv();
          BoxDiv.class('BoxDiv');
          BoxDiv.parent(SmallRow)
          L_Box[3*i+k][3*j+l] = BoxDiv;
        }
      }


    }
  }

  for (let i=0;i<9;i++){
    for (let j=0;j<9;j++){
      if (BoardInput[i][j] != '.'){
        L_Box[i][j].html(BoardInput[i][j]);
        L_Box[i][j].class('DontChangeDiv');
      } else {
        CanChange_List.push(i*9+j);
        L_Box[i][j].html('.')
        L_Box[i][j].class('CanChangeDiv');
        L_Box[i][j].mouseClicked(x => {MakeSetValueWindow(L_Box[i][j],i,j)});
      }
      L_Box[i][j].style('font-size','30px')
    }
  }
}

function CheckAllOK(){
  let AllDone = true;
  for (let i=0;i<CanChange_List.length;i++){
    if (BoardSimList[CanChange_List[i]].Value == null){
      AllDone = false;
    }
    if (BoardSimList[CanChange_List[i]].CheckOK()){
      L_Box[Math.floor(CanChange_List[i]/9)][CanChange_List[i]%9].style('background-color','#FFFFFF')
    } else {
      L_Box[Math.floor(CanChange_List[i]/9)][CanChange_List[i]%9].style('background-color','#FF0000')
      AllDone = false;
    }
  }
  if (AllDone){
    console.log('WIN')
  }
  return AllDone
}

function MakeSetValueWindow(L_Box_Input,row,col){
  if (SetValueWindow != null){
    SetValueWindow.remove();
  }
  SetValueWindow = createDiv();
  SetValueWindow.style('top',mouseY+'px');
  SetValueWindow.style('left',mouseX+'px');
  SetValueWindow.id('SetValueWindow');
  for (let i=0;i<3;i++){
    let ButRow = createDiv();
    ButRow.parent(SetValueWindow);
    for (let j=0;j<3;j++){
      SetBut = createButton(i*3+j+1);
      SetBut.parent(ButRow);
      SetBut.mouseClicked(x => {
        L_Box_Input.html(i*3+j+1);
        BoardSimList[row*9+col].SetValue(i*3+j+1);
        CheckAllOK();
        SetValueWindow.remove();
      })
    }
  }
  let ButNull = createButton('.');
  ButNull.parent(SetValueWindow);
  ButNull.style('width','70%');
  ButNull.mouseClicked(x => {
    L_Box_Input.html('.');
    L_Box_Input.style('background-color','#FFFFFF')
    BoardSimList[row*9+col].SetValue(null);
    CheckAllOK();
    SetValueWindow.remove();
  })
  let ButClose = createButton('X');
  ButClose.parent(SetValueWindow);
  ButClose.style('width','30%');
  ButClose.mouseClicked(x => {
    SetValueWindow.remove();
  })
}

var AnsBoard;
function GetAns(){
  let TestL = BoardInput
  L_BoardStack = [TestL];
  while (L_BoardStack.length != 0){
    let L_BoardPop = L_BoardStack.pop();
    let BoardSet_Now = new BoardSet(L_BoardPop);
    let L_Board_A = BoardSet_Now.Check();
    if (L_Board_A != false){
      if (L_Board_A[0] == 'Ans'){
        L_BoardStack = [];
        AnsBoard = L_Board_A[1]
      } else {
        for (let i = 0;i<L_Board_A.length;i++){
          L_BoardStack.push(L_Board_A[i]);
        }
      }
    }
  }
  for (let i=0;i<CanChange_List.length;i++){
    L_Box[Math.floor(CanChange_List[i]/9)][CanChange_List[i]%9].html(AnsBoard[Math.floor(CanChange_List[i]/9)][CanChange_List[i]%9])
    BoardSimList[CanChange_List[i]].SetValue(parseInt(AnsBoard[Math.floor(CanChange_List[i]/9)][CanChange_List[i]%9]));
    CheckAllOK()
  }
}
