#include <string>

using namespace std;
int ch;

char KBCheck(char MoveChar) {
	if (_kbhit()) {
		ch = _getch();
		if (ch == 100 && MoveChar!= 'W') {
			return 'E';
			
		}
		else if (ch == 115 && MoveChar != 'N') {
			return 'S';
		}
		else if (ch == 97 && MoveChar != 'E') {
			return 'W';
		}
		else if (ch == 119 && MoveChar != 'S') {
			return 'N';
		}
	}

	return MoveChar;
};