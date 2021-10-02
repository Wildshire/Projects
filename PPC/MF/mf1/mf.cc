/*
This is the function you need to implement. Quick reference:
- input rows: 0 <= y < ny
- input columns: 0 <= x < nx
- element at row y and column x is stored in in[x + y*nx]
- for each pixel (x, y), store the median of the pixels (a, b) which satisfy
  max(x-hx, 0) <= a < min(x+hx+1, nx), max(y-hy, 0) <= b < min(y+hy+1, ny)
  in out[x + y*nx].
*/
//Libraries
#include<algorithm>
void mf(int ny, int nx, int hy, int hx, const float *in, float *out) {
	//Auxiliary variables
	//For looping
	int row;//Through images
	int column;//Through image
	int x; //Through window
	int y; //Through window
	int i; //indexing window
	
	//Boundaries
	int min_boundary_y=0;
	int max_boundary_y=ny;
	int min_boundary_x=0;
	int max_boundary_x=nx;
	
	//For storing
	float median;
	float median_1;
	float median_2;
	int pos;
	
	//Loop for all pixels
	for(row=0;row<ny;row++){
		for(column=0;column<nx;column++){
			//Create window
			float *window = new float [(2*hx+1) * (2*hy+1)];
			i=0; //Index of the window
			//Loop through neighbors
			for(y=row-hy;y<row+hy+1;y++){
				for(x=column-hx;x<column+hx+1;x++){
					//printf("Values of y and x: %i,%i \n",y,x);
					//Check window pixel inside boundary
					if(y>=min_boundary_y && y<max_boundary_y && x>=min_boundary_x && x<max_boundary_x){
						//Then we can store pixel
						window[i] = in[x + y*nx];
						//for next position
						i++;
					}
								
				}
			}
			//printf("Number of elements: %i \n",i);
			//Calculate median
			//If window has odd elements
			if(i%2==1){
				pos=(i/2);
				std::nth_element(window,window + pos,window + i);
				median=window[pos];
			}
			//It has even elements
			else{
				pos=(i/2)-1;
				std::nth_element(window,window + (pos+1),window + i);
				median_1=window[pos+1];
				std::nth_element(window,window + pos,window + (pos+1));
				median_2=window[pos];
				median=(median_1+median_2)/2.0f;
			}
			//printf("The median is: %f",median);
			//Store value
			out[column + row*nx]=median;
			//Erase window
			delete[] window;
		}
	}
}
