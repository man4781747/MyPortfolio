const ButtomBodyBackGroundColor_Type0 = "rgb(91, 183, 76)"
const ButtomBodyBackGroundColor_Type1 = "#f25c54"
const ButtomBodyBackGroundColor_Type2 = "#ff9505"
const ButtomBodyBackGroundColor_Type3 = "#CCCCCC"

const ButtomTopBorderColor_Type0 = "rgb(160,243,85)"
const ButtomTopBorderColor_Type1 = "#f7b267"
const ButtomTopBorderColor_Type2 = "#ffc971"
const ButtomTopBorderColor_Type3 = "#959D92"

const ButtomTopBackGroundColor_Type0 = "rgb(142, 222, 92)"
const ButtomTopBackGroundColor_Type1 = "#f4845f"
const ButtomTopBackGroundColor_Type2 = "#ffb627"
const ButtomTopBackGroundColor_Type3 = "#DDDDDD"

var app = new Vue({
	el: '#app',
	data: {
		message: 'Hello Vue!',
		windowNum_row : 10,
		windowNum_col : 20,
		BoxList : [],
		BombNum : 20,
		GuestNum : 0,
		isShow : true,
		passCount : 0,
		gameStat : 'Win',
		gameIng : true,
		RandonBombPosition_set : null,
		ResetButton : {
			"text" : "0ω0",
			'text_save' : "0ω0",
			"buttom_body_height" : 170/20,
			"buttom_body_translateY" : 0,
			"buttom_body_height_save" : 170/20,
			"buttom_body_translateY_save" : 0,
			"buttom_body_background_color" : ButtomBodyBackGroundColor_Type0,
			"buttom_top_font_color" : "#EEEEEE",
			"buttom_top_border_color" : ButtomTopBorderColor_Type0,
			"buttom_top_background_color" : ButtomTopBackGroundColor_Type0,
		},
	},
	
	computed: {
		availWidth : function(){
			return window.screen.availWidth
		},
		availHeight : function(){
			return window.screen.availHeight 
		},
		BombCountDigits : function(){
			return this.BombNum % 10
		},
		BombCountTens : function(){
			return Math.floor(this.BombNum / 10)
		},
		BombGuestDigits : function(){
			return this.GuestNum % 10
		},
		BombGuestTens : function(){
			return Math.floor(this.GuestNum / 10)
		},
	},
	
	methods: {
		CheckWin: function () {
			if (this.passCount == this.BoxList.length - this.BombNum){
				this.gameStat = "Win"
				this.PopAllBomb(false)
				this.gameIng = false
				this.ButtomBodyChangeColorStyle(
					this.ResetButton,
					ButtomBodyBackGroundColor_Type2,
					ButtomTopBackGroundColor_Type2,
					ButtomTopBorderColor_Type2
				)
				this.ResetButton['text'] = '(✪ω✪)'
				this.ResetButton['text_save'] = '(✪ω✪)'
			}
		},
		INITCoolWindowPosition: function () {
			this.ButtomBodyChangeColorStyle(
				this.ResetButton,
				ButtomBodyBackGroundColor_Type0,
				ButtomTopBackGroundColor_Type0,
				ButtomTopBorderColor_Type0
			)
			this.ResetButton['text'] = '0w0'
			this.ResetButton['text_save'] = '0w0'
			this.gameStat = ""
			this.gameIng = true
			this.RandonBombPosition_set = new Set()
			this.GuestNum = 0
			this.passCount = 0
			while (this.RandonBombPosition_set.size < this.BombNum){
				var k=Math.round(Math.random()*this.windowNum_row*this.windowNum_col);
				if (!this.RandonBombPosition_set.has(k)){
					this.RandonBombPosition_set.add(k)
				}
			}
			
			// console.log(RandonBombPosition_set)
			
			this.BoxList = []
			for (let boxIndex_row=0;boxIndex_row<this.windowNum_row;boxIndex_row++){
				// this.BoxList.push([])
				for (let boxIndex_col=0;boxIndex_col<this.windowNum_col;boxIndex_col++){
					this.BoxList.push({
						"text": '',
						"type": 3,
						"left" : (boxIndex_col*204+40)/20,
						"top" : (boxIndex_row*162+250)/20,
						"buttom_body_height" : 170/20,
						"buttom_body_translateY" : 0,
						"buttom_body_height_save" : 170/20,
						"buttom_body_translateY_save" : 0,
						"buttom_body_background_color" : ButtomBodyBackGroundColor_Type3,
						"buttom_top_font_color" : "#EEEEEE",
						"buttom_top_border_color" : ButtomTopBorderColor_Type3,
						"buttom_top_background_color" : ButtomTopBackGroundColor_Type3,
						"style": "",
						"Bomb": this.RandonBombPosition_set.has(boxIndex_row*this.windowNum_col+boxIndex_col),
						"AroundNum": 0,
						"AroundGroup": [],
					})
				}
			}
			
			for (let boxIndex_row=0;boxIndex_row<this.windowNum_row;boxIndex_row++){
				for (let boxIndex_col=0;boxIndex_col<this.windowNum_col;boxIndex_col++){
					let thisBoxIndex = boxIndex_row*this.windowNum_col+boxIndex_col
					if (boxIndex_col == 0){
						for (let aroundIndex of [
							1,
							this.windowNum_col,this.windowNum_col+1,
							-this.windowNum_col,-this.windowNum_col+1,
						]){
							if (this.BoxList[thisBoxIndex+aroundIndex]!=undefined){
								this.BoxList[thisBoxIndex]["AroundGroup"].push(
									this.BoxList[thisBoxIndex+aroundIndex]
								)
								if (this.BoxList[thisBoxIndex+aroundIndex]["Bomb"]){
									this.BoxList[thisBoxIndex]["AroundNum"] += 1
								}
							}
						}
					}
					else if (boxIndex_col == this.windowNum_col - 1){
						for (let aroundIndex of [
							-1,
							this.windowNum_col-1,this.windowNum_col,
							-this.windowNum_col-1,-this.windowNum_col,
						]){
							if (this.BoxList[thisBoxIndex+aroundIndex]!=undefined){
								this.BoxList[thisBoxIndex]["AroundGroup"].push(
									this.BoxList[thisBoxIndex+aroundIndex]
								)
								if (this.BoxList[thisBoxIndex+aroundIndex]["Bomb"]){
									this.BoxList[thisBoxIndex]["AroundNum"] += 1
								}
							}
						}
					}
					else {
						for (let aroundIndex of [
							1,
							-1,
							this.windowNum_col-1,this.windowNum_col,this.windowNum_col+1,
							-this.windowNum_col-1,-this.windowNum_col,-this.windowNum_col+1,
						]){
							if (this.BoxList[thisBoxIndex+aroundIndex]!=undefined){
								this.BoxList[thisBoxIndex]["AroundGroup"].push(
									this.BoxList[thisBoxIndex+aroundIndex]
								)
								if (this.BoxList[thisBoxIndex+aroundIndex]["Bomb"]){
									this.BoxList[thisBoxIndex]["AroundNum"] += 1
								}
							}
						}
					}
					

					// this.BoxList[thisBoxIndex]['text'] = this.BoxList[thisBoxIndex]["AroundNum"]
				}
			}
			
			
			
		},
		
		GiveCoolWindowNewPosition: function () {
			for (BoxDatas of this.BoxList){
				let new_left = Math.floor(Math.random() * 100)
				let new_top = Math.floor(Math.random() * 100)
				BoxDatas['r_left'] = Math.floor((BoxDatas['left'] - new_left)/10)
				BoxDatas['r_top'] = Math.floor((BoxDatas['top'] - new_top)/10)
				BoxDatas['left'] = new_left
				BoxDatas['top'] = new_top
				
			}
		},
		
		ChangeButtomTopFontColor: function(buttomData, S_color){
			buttomData['buttom_top_font_color'] = S_color
		},
		
		ButtomClicked: function(buttomData, IfLeftClick){
			// Type : 0 已成功
			// Type : 1 已失敗
			// Type : 2 考慮
			// Type : 3 初始
			if (this.gameIng == false){
				
			}
			else if ((buttomData['type'] == 3 | buttomData['type'] == 2) & IfLeftClick & buttomData.Bomb){
				// 變紅
				if (buttomData['type'] == 2){
					this.GuestNum -= 1
				}
				
				this.ButtomBodyChangeColorStyle(
					buttomData,
					ButtomBodyBackGroundColor_Type1,
					ButtomTopBackGroundColor_Type1,
					ButtomTopBorderColor_Type1
				)
				this.ButtomTextChange(buttomData, ">ω<")
				this.ChangeButtomTopFontColor(buttomData, buttomData.buttom_body_background_color)
				buttomData['buttom_body_height'] = 190/20
				buttomData['buttom_body_translateY'] = -20/20
				buttomData['buttom_body_height_save'] = 190/20
				buttomData['buttom_body_translateY_save'] = -20/20
				buttomData['type'] = 1
				this.gameStat = "Lose"
				this.PopAllBomb(IfLeftClick)
				
				this.ButtomBodyChangeColorStyle(
					this.ResetButton,
					ButtomBodyBackGroundColor_Type1,
					ButtomTopBackGroundColor_Type1,
					ButtomTopBorderColor_Type1
				)
				this.ResetButton['text'] = '>ω<'
				this.ResetButton['text_save'] = '>ω<'
			} 
			else if ((buttomData['type'] == 2 | buttomData['type'] == 3) & IfLeftClick & !buttomData.Bomb){
				// 變綠
				if (buttomData['type'] == 2){
					this.GuestNum -= 1
				}
				
				this.ButtomBodyChangeColorStyle(
					buttomData,
					ButtomBodyBackGroundColor_Type0,
					ButtomTopBackGroundColor_Type0,
					ButtomTopBorderColor_Type0
				)
				// this.ButtomTextChange(buttomData, "0ω0")
				this.ButtomTextChange(buttomData, (buttomData['AroundNum'] == 0)?"":buttomData['AroundNum'])
				this.ChangeButtomTopFontColor(buttomData, buttomData.buttom_body_background_color)
				buttomData['buttom_body_height'] = 140/20
				buttomData['buttom_body_translateY'] = 30/20
				buttomData['buttom_body_height_save'] = 140/20
				buttomData['buttom_body_translateY_save'] = 30/20
				buttomData['type'] = 0
				if (buttomData['AroundNum'] == 0){
					for (let aroundBoxChose of buttomData['AroundGroup']){
						this.ButtomClicked(aroundBoxChose, IfLeftClick)
						this.ButtomMouseLeave(aroundBoxChose)
					}
				}
				this.passCount += 1
				this.CheckWin()
			} 
			else if ((buttomData['type'] == 3) & !IfLeftClick){
				// 變黃
				this.GuestNum += 1
				this.ButtomBodyChangeColorStyle(
					buttomData,
					ButtomBodyBackGroundColor_Type2,
					ButtomTopBackGroundColor_Type2,
					ButtomTopBorderColor_Type2
				)
				this.ButtomTextChange(buttomData, "- ω -")
				this.ChangeButtomTopFontColor(buttomData, buttomData.buttom_body_background_color)
				buttomData['buttom_body_height'] = 170/20
				buttomData['buttom_body_translateY'] = 0
				buttomData['buttom_body_height_save'] = 170/20
				buttomData['buttom_body_translateY_save'] = 0
				buttomData['type'] = 2
			}
			else if ((buttomData['type'] == 2) & !IfLeftClick){
				// 黃轉灰
				this.GuestNum -= 1
				this.ButtomBodyChangeColorStyle(
					buttomData,
					ButtomBodyBackGroundColor_Type3,
					ButtomTopBackGroundColor_Type3,
					ButtomTopBorderColor_Type3
				)
				this.ButtomTextChange(buttomData, "")
				this.ChangeButtomTopFontColor(buttomData, buttomData.buttom_body_background_color)
				buttomData['buttom_body_height'] = 170/20
				buttomData['buttom_body_translateY'] = 0
				buttomData['buttom_body_height_save'] = 170/20
				buttomData['buttom_body_translateY_save'] = 0
				buttomData['type'] = 3
			}
		},
		
		ButtomMouseOver: function(buttomData, S_color){
			this.ChangeButtomTopFontColor(buttomData, buttomData.buttom_body_background_color)
			if (buttomData['type'] != 0){
				buttomData['buttom_body_height'] = 190/20
				buttomData['buttom_body_translateY'] = -20/20
			}
		},
		
		ButtomMouseLeave: function(buttomData, S_color){
			this.ChangeButtomTopFontColor(buttomData, "#EEEEEE")
			this.ButtomMouseUp(buttomData)
		},
		
		ButtomTextChange: function(buttomData, S_Text){
			buttomData['text'] = S_Text
		},
		
		ButtomBodyChangeColorStyle: function(buttomData, S_bodyColor, S_topColor, S_topBorderColor){
			buttomData['buttom_body_background_color'] = S_bodyColor
			buttomData['buttom_top_background_color'] = S_topColor
			buttomData['buttom_top_border_color'] = S_topBorderColor
		},
		
		ButtomMouseDown: function(buttomData){
			buttomData['buttom_body_height'] = 150/20
			buttomData['buttom_body_translateY'] = 20/20
			this.ResetButton['text'] = '(ﾉ>ω<)ﾉ'
		},
		
		ButtomMouseUp: function(buttomData){
			buttomData['buttom_body_height'] = buttomData['buttom_body_height_save']
			buttomData['buttom_body_translateY'] = buttomData['buttom_body_translateY_save']
			this.ResetButton['text'] = this.ResetButton['text_save']
		},
		
		PopAllBomb: function(IfLeftClick){
			for (let BombIndex of this.RandonBombPosition_set){
				this.ButtomClicked(this.BoxList[BombIndex], IfLeftClick)
				this.ButtomMouseLeave(this.BoxList[BombIndex])
			}
			this.gameIng = false
		},
	
		ResetButtonClick: function(){
			// this.ButtomBodyChangeColorStyle(
				// this.ResetButton,
				// ButtomBodyBackGroundColor_Type0,
				// ButtomTopBackGroundColor_Type0,
				// ButtomTopBorderColor_Type0
			// )
			// this.ResetButton['text'] = '0w0'
			// this.ResetButton['text_save'] = '0w0'
			this.INITCoolWindowPosition()
		},
		
		BombNumChange: function(I_numChange){
			this.BombNum += I_numChange
			if (this.BombNum <0) {
				this.BombNum = 0
			} else if (this.BombNum > 99) {
				this.BombNum = 99
			}
			this.INITCoolWindowPosition()
		},
	},
	
})

app.INITCoolWindowPosition()
// app.GiveCoolWindowNewPosition()