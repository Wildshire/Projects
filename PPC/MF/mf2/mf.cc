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
#include<vector>

void mf(int ny, int nx, int hy, int hx, const float *in, float *out) {
	//Auxiliary variables
	
	//Boundaries
	int min_boundary_y=0;
	int max_boundary_y=ny;
	int min_boundary_x=0;
	int max_boundary_x=nx;
	
	//Loop for all pixels
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ny;++row){
		for(int column=0;column<nx;++column){
			//Create window
			std::vector<float> window ((2*hx+1) * (2*hy+1),0.0);
			int i=0; //Index of the window
			//Loop through neighbors
			for(int y=row-hy;y<row+hy+1;++y){
				for(int x=column-hx;x<column+hx+1;++x){
					//Check window pixel inside boundary
					if(y>=min_boundary_y && y<max_boundary_y && x>=min_boundary_x && x<max_boundary_x){
						//Then we can store pixel
						window[i] = in[x + y*nx];
						//for next position
						i++;
					}
								
				}
			}
			//Calculate median
			//If window has odd elements
			float median=0.0;
			float median_1=0.0;
			float median_2=0.0;
			int pos=0;
			if(i%2==1){
				pos=(i/2);
				std::nth_element(window.begin(),window.begin() + pos,window.begin() + i);
				median=window[pos];
			}
			//It has even elements
			else{
				pos=(i/2)-1;
				std::nth_element(window.begin(),window.begin() + (pos+1),window.begin() + i);
				median_1=window[pos+1];
				std::nth_element(window.begin(),window.begin() + pos,window.begin() + (pos+1));
				median_2=window[pos];
				median=(median_1+median_2)/2.0f;
			}
			//Store value
			out[column + row*nx]=median;
		}
	}
}
