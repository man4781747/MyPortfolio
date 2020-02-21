#include <string>

using namespace std;

class PlayerBug {
public:
	int I_x;
	int I_y;
	char C_Type;
	class PlayerBug *next = NULL;
	class PlayerBug *previous = NULL;

	//int[2] GetXY() {
	//	int ReturnAns[2] = {I_x,I_y};
	//	return ReturnAns;
	//};
	//void GetXY(int, int)
	void ChangeXY(int I_x_input, int I_y_input) {
		I_x = I_x_input;
		I_y = I_y_input;
	}

	int GetX(void) {
		return I_x;
	}

	int GetY(void) {
		return I_y;
	}
};

//void PlayerBug::GetXY() {
//	return { I_x, I_y };
//}