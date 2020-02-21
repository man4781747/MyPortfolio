// ConsoleApplication2.cpp : 此檔案包含 'main' 函式。程式會於該處開始執行及結束執行。
//

#include <iostream>
#include <stdlib.h> 
#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include "GameReset.h"
#include "KBControl.h"


void goto_xy(int x, int y)//定位游標位置到指定座標
{
	HANDLE hOut;
	hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	COORD pos = { x,y };
	SetConsoleCursorPosition(hOut, pos);
}

int main()
{
	int i, j, k;
	int LastX, LastY;
	char ch;
	GameReset();


	while (1) {
		if (GameMode == 'S') {
			// 削去遊戲場資訊(除了牆壁)
			for (i = 1; i < GroundHight - 1; i++) {
				for (j = 1; j < GroundWide - 1; j++) {
					BaseGround[i][j] = ' ';
				}
			}

			GameReset();
			goto_xy(0, 0);
			//system("cls");
			for (i = 0; i < 21; i++) {
				BaseGround[8][10 + i] = GAMESTARTChar[i];
			}
			for (i = 0; i < sizeof(GAMEINSTRUCTIONChar); i++) {
				BaseGround[12][7 + i] = GAMEINSTRUCTIONChar[i];
			}
			for (i = 0; i < GroundHight; i++) {
				for (j = 0; j < GroundWide; j++) {
					printf("%c", BaseGround[i][j]);
				}
				printf("\n");
			}
			char ch;
			_getch();
			GameMode = 'I';
		}

		if (GameMode == 'I') {
			int LoopCount = 0;
			while (LoopCount < GameSpeed) {
				NowDirection = KBCheck(NowDirection);
				LoopCount += 1;
			}
			// 削去遊戲場資訊(除了牆壁)
			for (i = 1; i < GroundHight - 1; i++) {
				for (j = 1; j < GroundWide - 1; j++) {
					BaseGround[i][j] = ' ';
				}
			}

			// 記錄即將改變的最末尾XY值
			LastX = P_PlayerBugTail->I_x;
			LastY = P_PlayerBugTail->I_y;

			PlayerBodyChosePointer = P_PlayerBugTail;
			P_PlayerBodyChose_Pre = PlayerBodyChosePointer->previous;
			while (P_PlayerBodyChose_Pre != NULL) {
				PlayerBodyChosePointer->ChangeXY(
					P_PlayerBodyChose_Pre->GetX(),
					P_PlayerBodyChose_Pre->GetY()
				);
				BaseGround[PlayerBodyChosePointer->I_y][PlayerBodyChosePointer->I_x] = PlayerBodyChosePointer->C_Type;
				PlayerBodyChosePointer = PlayerBodyChosePointer->previous;
				P_PlayerBodyChose_Pre = P_PlayerBodyChose_Pre->previous;
			}

			if (NowDirection == 'E') {
				PlayerBodyChosePointer->I_x += 1;
			}
			else if (NowDirection == 'W') {
				PlayerBodyChosePointer->I_x -= 1;
			}
			else if (NowDirection == 'S') {
				PlayerBodyChosePointer->I_y += 1;
			}
			else if (NowDirection == 'N') {
				PlayerBodyChosePointer->I_y -= 1;
			}

			if (
				BaseGround[PlayerBodyChosePointer->I_y][PlayerBodyChosePointer->I_x] == '*' ||
				BaseGround[PlayerBodyChosePointer->I_y][PlayerBodyChosePointer->I_x] == 'B'
				) {
				GameMode = 'D';
			}

			if (PlayerBodyChosePointer->I_y == Class_Apple.I_y & PlayerBodyChosePointer->I_x == Class_Apple.I_x) {
				score += 1;
				SnackLong += 1;
				GameSpeed -= 300;
				if (GameSpeed <= 1) {
					GameSpeed = 1;
				}
				Class_Apple.C_live = 'F';
				BaseGround[LastY][LastX] = 'B';
				PlayerBug *PlayerBodyNew = new PlayerBug();
				PlayerBodyNew->I_x = LastX;
				PlayerBodyNew->I_y = LastY;
				PlayerBodyNew->C_Type = 'B';
				PlayerBodyNew->previous = P_PlayerBugTail;
				P_PlayerBugTail->next = PlayerBodyNew;
				P_PlayerBugTail = P_PlayerBugTail->next;
			}

			BaseGround[PlayerBodyChosePointer->I_y][PlayerBodyChosePointer->I_x] = PlayerBodyChosePointer->C_Type;

			if (Class_Apple.C_live == 'F') {
				Class_Apple.ChangePosition(P_BaseGround, SnackLong, GroundWide, GroundHight);
			}
			BaseGround[Class_Apple.I_y][Class_Apple.I_x] = 'A';

			//_getch();
			 //繪製最終圖形
			char test[(GroundWide + 1)*GroundHight + 1];
			for (i = 0; i < GroundHight; i++) {
				for (j = 0; j < GroundWide; j++) {
					test[i*(GroundWide + 1) + j] = BaseGround[i][j];
				}
				test[i*(GroundWide + 1) + j] = '\n';
			}
			test[(GroundWide + 1)*GroundHight] = '\0';

			//system("cls");
			goto_xy(0, 0);
			printf("%s", test);

			printf(" 你現在的總長度 : %d  得分 : %d", SnackLong, score);
		}
		if (GameMode == 'D') {
			system("cls");
			for (i = 0; i < sizeof(GAMEOVERChar); i++) {
				BaseGround[9][5 + i] = GAMEOVERChar[i];
			}
			for (i = 0; i < GroundHight; i++) {
				for (j = 0; j < GroundWide; j++) {
					printf("%c", BaseGround[i][j]);
				}
				printf("\n");
			}
			printf("  你最後的總長度 : %d  得分 : %d", SnackLong, score);
			_getch();
			GameMode = 'S';
		}
	}
}

// 執行程式: Ctrl + F5 或 [偵錯] > [啟動但不偵錯] 功能表
// 偵錯程式: F5 或 [偵錯] > [啟動偵錯] 功能表

// 開始使用的提示: 
//   1. 使用 [方案總管] 視窗，新增/管理檔案
//   2. 使用 [Team Explorer] 視窗，連線到原始檔控制
//   3. 使用 [輸出] 視窗，參閱組建輸出與其他訊息
//   4. 使用 [錯誤清單] 視窗，檢視錯誤
//   5. 前往 [專案] > [新增項目]，建立新的程式碼檔案，或是前往 [專案] > [新增現有項目]，將現有程式碼檔案新增至專案
//   6. 之後要再次開啟此專案時，請前往 [檔案] > [開啟] > [專案]，然後選取 .sln 檔案
