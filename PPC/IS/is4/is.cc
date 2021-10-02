//Imports
#include <limits>
#include <cstdio>
#include <vector>
#include <tuple>
#include <omp.h>


//Time for vectorization
//Creating vectors of 4 doubles
typedef double double4_t __attribute__ ((vector_size (4*sizeof(double))));

//Creating pointer of vectors alligning with memory, book example
double4_t * double4_alloc(std::size_t n){
        void * tmp=0;
        if(posix_memalign(&tmp,sizeof(double4_t),sizeof(double4_t)*n)){
                throw std::bad_alloc();
        }
        return (double4_t *) tmp;
}


//Struct given by exercise
struct Result {
    int y0;
    int x0;
    int y1;
    int x1;
    float outer[3];
    float inner[3];
};

/*
This is the function you need to implement. Quick reference:
- x coordinates: 0 <= x < nx
- y coordinates: 0 <= y < ny
- color components: 0 <= c < 3
- input: data[c + 3 * x + 3 * nx * y]
*/



Result segment(int ny, int nx, const float *data) {
	//Aux variables
	Result result{0, 0, 0, 0, {0, 0, 0}, {0, 0, 0}}; //The result
	int colors=3; //We have 3 colors
	int total_pixels=ny*nx; //Total number of pixels
	double4_t double4_0={0.0,0.0,0.0,0.0}; //Zero vector
	double top_error=std::numeric_limits<double>::infinity(); //Maximum error

	//Preparations of the vectors vectorized +1 capicity for padding
	double4_t * sums = double4_alloc((ny+1)*(nx+1));
	
	double sq_sum = 0.0; //This is going to have values squared, constant summed to the error

	//Initialize sums, all to zero
	for(int pixel_y=0;pixel_y<=ny;++pixel_y){
		for(int pixel_x=0;pixel_x<=nx;++pixel_x){
			for(int c=0;c<colors+1;++c){
				sums[(nx+1)*pixel_y+pixel_x][c]=0.0;
			}
		}
	}
		
	
	//Preprocess all sums
	for(int pixel_y=0;pixel_y<ny;++pixel_y){
		for(int pixel_x=0;pixel_x<nx;++pixel_x){
			for(int c=0;c<colors+1;++c){
				//We do not want c>4 to access data
				if(c<3){
					sums[(pixel_y+1)*(nx+1)+pixel_x+1][c]=data[c + 3 * pixel_x + 3 * nx * pixel_y];
					sq_sum=(data[c + 3 * pixel_x + 3 * nx * pixel_y]*data[c + 3 * pixel_x + 3 * nx * pixel_y])+sq_sum;
				}
				else{
					sums[(pixel_y+1)*(nx+1)+pixel_x+1][c]=0.0;
				}
			}
			//we have calulated the ones before and we can do 3 channels at the same time
			sums[(nx+1)*(pixel_y+1)+pixel_x+1]+=sums[(nx+1)*(pixel_y+1)+pixel_x]+(sums[(nx+1)*pixel_y+(pixel_x+1)]-sums[(nx+1)*pixel_y+pixel_x]);
		}
	}
	
	//Time to do heavy computation
	#pragma omp parallel
	{ 
		double local_error=top_error; //Local error for each thread
		//Final positions and values of best rectangle found by thread
		int final_y1=0; 
		int final_x1=0;
		int final_y0=0;
		int final_x0=0;
		double4_t final_internal_values = double4_0;
		double4_t final_external_values = double4_0;
		//This is the bottom right sum of all the picture, we are going to access this guy, a lot, better to keep it precomputated
		double4_t total=sums[(nx+1)*ny+nx];
		//Time to do loops, first: draw rectangle, then, we move it around all possible positions 
		#pragma omp for nowait schedule (dynamic,1)
		for(int height=1;height<=ny;++height){
			for(int width=1;width<=nx;++width){
				//Get as much info of the current rectangle before moving it around
				int rectangle_pixels=height*width;
				double rectangle_pixels_2=1.0; //Auxiliar for the division
				int rest_pixels=total_pixels-rectangle_pixels; //The rest
				double rest_pixels_2=1.0; //Auxiliar
				//Preprocess these guys to do less divisions
				if(rectangle_pixels!=0){
					rectangle_pixels_2=1.0/rectangle_pixels;
				}
				if(rest_pixels!=0){
					rest_pixels_2=1.0/rest_pixels;
				}
				//Move rectangle around
				for(int y0=1,y1=height+1;y0<=ny && y1<=ny+1;++y0,++y1){
					for(int x0=1,x1=width+1;x0<=nx && x1<=nx+1;++x0,++x1){
						//We have the rectangle, time to figure out the sum of the internal and external values
						double4_t internal_values=double4_0;
						double4_t external_values=double4_0;
						//The idea of the internal sum is bottom_right-top_right-bottom_left+top_left
						double4_t bottom_right=double4_0;
						double4_t top_right=double4_0;
						double4_t bottom_left=double4_0;
						double4_t top_left=double4_0;
						//Internal stuff
						bottom_right=sums[(nx+1)*(y1-1)+x1-1];
						top_right=sums[(nx+1)*(y0-1)+x1-1];
						bottom_left=sums[(nx+1)*(y1-1)+x0-1];
						top_left=sums[(nx+1)*(y0-1)+x0-1];
						//Calculations
						internal_values=(bottom_right-top_right)+(top_left-bottom_left);
						external_values=total-internal_values;
					

						//Give rectangle the values, and I swap the operation to multiplication
						internal_values*=rectangle_pixels_2;
						external_values*=rest_pixels_2;

						//Now we calculate the cost of the each channel at the same time
						double4_t error=double4_0;
						error=(error+sq_sum)+((internal_values*internal_values)*(-1)*rectangle_pixels)+((external_values*external_values)*(-1)*rest_pixels);
						//Sum the elements of error vector of the 3 channels
						double final_error=0.0;
						for(int c=0;c<colors;++c){
							final_error+=error[c];
						}
						//Update
						if(final_error<local_error){
							local_error=final_error;
							final_y1=y1-1;
							final_x1=x1-1;
							final_y0=y0-1;
							final_x0=x0-1;
							final_internal_values=internal_values;
							final_external_values=external_values;
						}
					}

				}
			}
		}
		//End of loop, now each thread will be checking if their solution is better than others, good to have no wait to create less of a bottleneck
		#pragma omp critical
		{
			if(local_error<top_error){
				//New threshold
				top_error=local_error;
				result.y0=final_y0;
				result.x0=final_x0;
				result.y1=final_y1;
    				result.x1=final_x1;
				for(int c=0;c<colors;++c){
					result.inner[c]=final_internal_values[c];
					result.outer[c]=final_external_values[c];
				}
			
			}	
		}
	
	}
	//End parallel
	
   	//Free sums
	std::free(sums); 
	//And return
	return result;
}
