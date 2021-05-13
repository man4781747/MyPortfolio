
var BoardSimList;

class Box_Sim {
  constructor(row, col){
    this.Value = null;
    this.I_Row = row;
    this.I_Col = col;
    this.RowGroup = null;
    this.ColGroup = null;
    this.BoxGroup = null;
    this.Maybe = new Set([1,2,3,4,5,6,7,8,9]);
  }

  SetValue(Value){
    this.Value = Value;
  }

  CheckOK(){
    if (this.RowGroup.Check()){
      if (this.ColGroup.Check()){
        if (this.BoxGroup.Check()){
          return true
        }
      }
    }
    return false
  }
}

class BoxGroup_Sim{
  constructor(){
    this.BoxMember = [];
  }
  Check(){
    let L_all = [];
    for(let NumChose = 0;NumChose<this.BoxMember.length;NumChose++){
      if(this.BoxMember[NumChose].Value){
        L_all.push(this.BoxMember[NumChose].Value);
      }
    }
    if (L_all.length != new Set(L_all).size){
      return false
    }
    return true
  }
}

class RowGroup_Sim{
  constructor(){
    this.RowMember = [];
  }
  Check(){
    let L_all = [];
    for(let NumChose = 0;NumChose<this.RowMember.length;NumChose++){
      if(this.RowMember[NumChose].Value){
        L_all.push(this.RowMember[NumChose].Value);
      }
    }

    if (L_all.length != new Set(L_all).size){
      return false
    }
    return true
  }
}

class ColGroup_Sim{
  constructor(){
    this.ColMember = [];
  }
  Check(){
    let L_all = [];
    for(let NumChose = 0;NumChose<this.ColMember.length;NumChose++){
      if(this.ColMember[NumChose].Value){
        L_all.push(this.ColMember[NumChose].Value);
      }
    }

    if (L_all.length != new Set(L_all).size){
      return false
    }
    return true
  }
}

class BoardSet_Sim{
  constructor(L_Board_Input){
    BoardSimList = [];
    this.AllBoxGroup = [];
    for (let col=0;col<3;col++){
      this.AllBoxGroup.push([]);
      for (let row=0;row<3;row++){
        this.AllBoxGroup[col].push(new BoxGroup_Sim());
      }
    }
    // this.AllBoxGroup = (new Array(3)).fill(new Array(3).fill(new BoxGroup()));
    this.AllRowGroup = [];
    for (let row=0;row<9;row++){
      this.AllRowGroup.push(new RowGroup_Sim())
    }

    this.AllColGroup = [];
    for (let row=0;row<9;row++){
      this.AllColGroup.push(new ColGroup_Sim())
    }

    for (let col=0;col<9;col++){
      for (let row=0;row<9;row++){
        BoardSimList.push(new Box_Sim(row,col));
        this.AllRowGroup[row].RowMember.push(BoardSimList[BoardSimList.length-1]);
        this.AllColGroup[col].ColMember.push(BoardSimList[BoardSimList.length-1]);
        this.AllBoxGroup[Math.floor(row/3)][Math.floor(col/3)].BoxMember.push(BoardSimList[BoardSimList.length-1]);
        BoardSimList[BoardSimList.length-1].BoxGroup = this.AllBoxGroup[Math.floor(row/3)][Math.floor(col/3)];
        BoardSimList[BoardSimList.length-1].ColGroup = this.AllColGroup[col];
        BoardSimList[BoardSimList.length-1].RowGroup = this.AllRowGroup[row];
      }
    }
    for (let col=0;col<9;col++){
      for (let row=0;row<9;row++){
        if (L_Board_Input[row][col] != '.'){
          BoardSimList[row*9+col].SetValue(parseInt(L_Board_Input[row][col]))
        }
      }
    }
  }

}
