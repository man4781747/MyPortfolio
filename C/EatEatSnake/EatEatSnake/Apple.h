#include <string>

using namespace std;
class Apple {
public:
	int I_x = -1;
	int I_y = -1;
	char C_live = 'F';

	void ChangePosition(char *Map, int SnackLong, int MapWide, int MapHight) {
		C_live = 'T';
		int PlayGroundSize = (MapWide - 2) * (MapHight - 2);
		int RandonChose = rand() % (PlayGroundSize - SnackLong);
		int CountNum = 0;
		while (RandonChose != 0) {
			if (*(Map + CountNum) == ' ') {
				RandonChose -= 1;
			}
			CountNum += 1;
		}
		CountNum -= 1;
		I_x = CountNum%MapWide;
		I_y = CountNum/MapWide;
	}
};
