#include "ccc_win.h"

int ccc_win_main(){
	
	Point top_left(-5, 5);
	Point top_right(5, 5);
	Point bottom_left(-5, -5);
	Point bottom_right(5, -5);
	Point a(-5, -1.66), b(5, -1.66), c(-5, 1.66), d(5, 1.66),e(-1.66,-5),f(-1.66,5),g(1.66,-5),h(1.66,5);

	Line horizontal1(top_left, top_right);
	Line horizontal2(bottom_left, bottom_right);
	Line vertical1(bottom_left, top_left);
	Line vertical2(bottom_right, top_right);
	Line vertical3(a, b);
	Line vertical4(c, d);
	Line horizontal5(e, f);
	Line horizontal6(g, h);
	cwin << horizontal1 << horizontal2 << vertical1 << vertical2 << vertical3 << vertical4 << horizontal5 << horizontal6;

	//Clicks
	
	int counter = 0, R = 1;
	double circx,circy,x1,x2,y1,y2;
	bool Continue = true;
	while (counter <= 9 && Continue)
	{
		Point click = cwin.get_mouse("click");
		double clickx = click.get_x();
		double clicky = click.get_y();
		if (-5 <= clickx && clickx <= -1.66)
		{
			circx = -3.33;
			x1 = -5;
			x2 = -1.66;
		}
		else if (-1.66 <= clickx && clickx <= 1.66)
		{
			circx = 0;
			x1 = -1.66;
			x2 = 1.66;
		}
		else if (1.66 <= clickx && clickx <= 5)
		{
			circx = 3.33;
			x1 = 1.66;
			x2 = 5;
		}
		//Check y
		if (-5 <= clicky && clicky <= -1.66)
		{
			circy = -3.33;
			y1 = -5;
			y2 = -1.66;
		}
		else if (-1.66 <= clicky && clicky <= 1.66)
		{
			circy = 0;
			y1 = -1.66;
			y2 = 1.66;
		}
		else if (1.66 <= clicky && clicky <= 5)
		{
			circy = 3.33;
			y1 = 1.66;
			y2 = 5;
		}
		
		counter++;
		
		if (counter % 2 == 0)
		{
			cwin << Line(Point(x1, y1), Point(x2, y2)) << Line(Point(x1, y2), Point(x2, y1));
		}
		else
		{
			cwin << Circle(Point(circx, circy), R);
		}
		
		if(counter==9)
		{
			if(cwin.get_string("Continue? Y for yes, N for no: ")=="Y")
			{
				Continue=true;
				cwin << horizontal1 << horizontal2 << vertical1 << vertical2 << vertical3 << vertical4 << horizontal5 << horizontal6;
				counter = 0
			}
			else
			{
				Continue=false;
			}
		}
		

	}
		
		return 0;
}
