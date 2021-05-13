var L_BoardStack;

class Box {
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
    if (this.Value == Value){
      return true
    }
    if (this.Maybe.has(Value) != true){

      this.Maybe = new Set([]);
      this.Value = null
      return false
    }
    this.Value = Value;
    this.Maybe = new Set([]);
    for (let NumChose=0;NumChose<this.BoxGroup.BoxMember.length;NumChose++){
      this.BoxGroup.BoxMember[NumChose].Maybe.delete(Value);
      if (this.BoxGroup.BoxMember[NumChose].Maybe.size == 1) {
        this.BoxGroup.BoxMember[NumChose].SetValue(this.BoxGroup.BoxMember[NumChose].Maybe.values().next().value);
      }
    }
    for (let NumChose=0;NumChose<this.RowGroup.RowMember.length;NumChose++){
      this.RowGroup.RowMember[NumChose].Maybe.delete(Value);
      if (this.RowGroup.RowMember[NumChose].Maybe.size == 1) {
        this.RowGroup.RowMember[NumChose].SetValue(this.RowGroup.RowMember[NumChose].Maybe.values().next().value);
      }
    }
    for (let NumChose=0;NumChose<this.ColGroup.ColMember.length;NumChose++){
      this.ColGroup.ColMember[NumChose].Maybe.delete(Value);
      if (this.ColGroup.ColMember[NumChose].Maybe.size == 1) {
        this.ColGroup.ColMember[NumChose].SetValue(this.ColGroup.ColMember[NumChose].Maybe.values().next().value);
      }
    }
    return true
  }
}

class BoxGroup{
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

class RowGroup{
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

class ColGroup{
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

class BoardSet{
  constructor(L_Board_Input){
    this.AllBox = [];
    this.AllBoxGroup = [];
    for (let col=0;col<3;col++){
      this.AllBoxGroup.push([]);
      for (let row=0;row<3;row++){
        this.AllBoxGroup[col].push(new BoxGroup());
      }
    }
    this.AllRowGroup = [];
    for (let row=0;row<9;row++){
      this.AllRowGroup.push(new RowGroup())
    }

    this.AllColGroup = [];
    for (let row=0;row<9;row++){
      this.AllColGroup.push(new ColGroup())
    }
    for (let col=0;col<9;col++){
      for (let row=0;row<9;row++){
        this.AllBox.push(new Box(row,col));
        this.AllRowGroup[row].RowMember.push(this.AllBox[this.AllBox.length-1]);
        this.AllColGroup[col].ColMember.push(this.AllBox[this.AllBox.length-1]);
        this.AllBoxGroup[Math.floor(row/3)][Math.floor(col/3)].BoxMember.push(this.AllBox[this.AllBox.length-1]);
        this.AllBox[this.AllBox.length-1].BoxGroup = this.AllBoxGroup[Math.floor(row/3)][Math.floor(col/3)];
        this.AllBox[this.AllBox.length-1].ColGroup = this.AllColGroup[col];
        this.AllBox[this.AllBox.length-1].RowGroup = this.AllRowGroup[row];
      }
    }
    for (let col=0;col<9;col++){
      for (let row=0;row<9;row++){
        if (L_Board_Input[row][col] != '.'){
          this.AllBox[row*9+col].SetValue(parseInt(L_Board_Input[row][col]))
        }
      }
    }
  }

  Check(){
    for (let col=0;col<3;col++){
      for (let row=0;row<3;row++){
        if (this.AllBoxGroup[col][row].Check() != true){
          return [];
        }
      }
    }
    for (let NumChose=0;NumChose<9;NumChose++){
      if (this.AllRowGroup[NumChose].Check() != true){
        return [];
      }
    }
    for (let NumChose=0;NumChose<9;NumChose++){
      if (this.AllColGroup[NumChose].Check() != true){
        return [];
      }
    }
    var GuestBox;
    let MinNum = 10;
    for (let NumChose=0;NumChose<this.AllBox.length;NumChose++){
      let I_Len_Maybe = this.AllBox[NumChose].Maybe.size;
      if (this.AllBox[NumChose].Value == null & I_Len_Maybe == 0){
        return []
      } else if (this.AllBox[NumChose].Value == null & I_Len_Maybe != 1) {
        if (I_Len_Maybe < MinNum){
          MinNum = I_Len_Maybe;
          GuestBox = this.AllBox[NumChose];
        }
      } else if (this.AllBox[NumChose].Value == null & I_Len_Maybe == 1){
        this.AllBox[NumChose].SetValue(this.AllBox[NumChose].Maybe.values().next().value);
      }
    }
    if (MinNum == 10) {
      console.log(this.OutputBoard())
      return (['Ans',this.OutputBoard()])
    } else {
      console.log('More Ans?');
      let L_MoreMaybeBoard = [];
      let AllMaybe = GuestBox.Maybe.values()
      for (let MaybeValueNum=0;MaybeValueNum<GuestBox.Maybe.size;MaybeValueNum++){
        let L_BaseBoard = this.OutputBoard();
        let Num = AllMaybe.next().value
        // console.log(String(Num))
        L_BaseBoard[GuestBox.I_Col][GuestBox.I_Row] = String(Num);
        L_MoreMaybeBoard.push(L_BaseBoard);
      }
      return L_MoreMaybeBoard
    }
  }

  OutputBoard(){
    let L_Board_O = [];
    for (let i=0;i<9;i++){
      L_Board_O.push([])
    }
    for (let row=0;row<9;row++){
      for (let col=0;col<9;col++){
        if (this.AllColGroup[row].ColMember[col].Value != null){
          L_Board_O[row].push(
            String(this.AllColGroup[row].ColMember[col].Value)
          )
        } else {
          L_Board_O[row].push('.')
        }
      }
    }
    return L_Board_O;
  }
}
