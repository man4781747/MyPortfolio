#include "PlayerBug.h"
#include "Apple.h"


PlayerBug PlayerBody;
PlayerBug *PlayerBugHeadPointer;
PlayerBug *P_PlayerBugTail;
PlayerBug *PlayerBodyChosePointer;
PlayerBug *PlayerBodyChosePointer_Next;
PlayerBug *P_PlayerBodyChose_Pre;
const int GroundWide = 40;
const int GroundHight = 20;
int SnackLong;
char NowDirection;
char *P_BaseGround;
using namespace std;
char BaseGround[GroundHight][GroundWide];
Apple Class_Apple;
char GameMode;
const char GAMESTARTChar[21] = "ANY PRESS GAME START";
const char GAMEINSTRUCTIONChar[] = "W:UP A:LEFT S:DOWN D:RIGHT";
const char GAMEOVERChar[] = "GAME OVER !! ANY PRESS TO RESET";
int score;
int GameSpeed;

void GameReset() {
	int k, i, j;
	GameSpeed = 3000;
	for (i = 0; i < GroundWide; i++) {
		BaseGround[0][i] = '*';
		BaseGround[GroundHight - 1][i] = '*';
	}
	for (j = 1; j < GroundHight; j++) {
		BaseGround[j][0] = '*';
		BaseGround[j][GroundWide - 1] = '*';
	}
	for (i = 1; i < GroundHight - 1; i++) {
		for (j = 1; j < GroundWide - 1; j++) {
			BaseGround[i][j] = ' ';
		}
	}
	GameMode = 'S';
	// 玩家初始蟲體資料
	SnackLong = 4;
	PlayerBody.I_x = GroundWide / 2;
	PlayerBody.I_y = GroundHight / 2;
	PlayerBody.C_Type = 'H';
	PlayerBugHeadPointer = &PlayerBody;
	PlayerBodyChosePointer = &PlayerBody;
	for (k = 0; k < SnackLong - 1; k++) {
		PlayerBug *PlayerBodyNext = new PlayerBug();
		PlayerBodyNext->I_x = PlayerBody.I_x - 1 - k;
		PlayerBodyNext->I_y = PlayerBody.I_y;
		PlayerBodyNext->C_Type = 'B';
		PlayerBodyChosePointer->next = PlayerBodyNext;
		PlayerBodyNext->previous = PlayerBodyChosePointer;
		PlayerBodyChosePointer = PlayerBodyNext;
	}
	P_PlayerBugTail = PlayerBodyChosePointer;

	NowDirection = 'E';
	P_BaseGround = &BaseGround[0][0];
	Class_Apple.C_live = 'F';
	score = 0;
}