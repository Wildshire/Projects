//Imports
#include <limits>
#include <cstdio>
#include <vector>
#include <tuple>
#include <omp.h>
#include <immintrin.h>

//Time for vectorization
//Creating vectors of 8 floats
typedef float float8_t __attribute__ ((vector_size (8*sizeof(float))));

//Creating pointer of vectors alligning with memory, book example
float8_t * float8_alloc(std::size_t n){
        void * tmp=0;
        if(posix_memalign(&tmp,sizeof(float8_t),sizeof(float8_t)*n)){
                throw std::bad_alloc();
        }
        return (float8_t *) tmp;
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
	int total_pixels=ny*nx; //Total number of pixels
	//float8_t float8_0={0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0}; //Zero vector
	float top_error=std::numeric_limits<float>::infinity(); //Maximum error

	//Preparations of the vectors vectorized +1 capicity for padding
	float8_t float8_0 = {0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};
	std::vector<float> sums((ny+1)*(nx+1+8),0.0);

	//Preprocess all sums
	for(int pixel_y=0;pixel_y<ny;++pixel_y){
		for(int pixel_x=0;pixel_x<nx;++pixel_x){
				//Get first channel only
				sums[(pixel_y+1)*(nx+1+8)+pixel_x+1]=data[0 + 3 * pixel_x + 3 * nx * pixel_y];
				//we have calulated the ones before and we can do 3 channels at the same time
				sums[(nx+1+8)*(pixel_y+1)+pixel_x+1]+=sums[(nx+1+8)*(pixel_y+1)+pixel_x]+(sums[(nx+1+8)*pixel_y+(pixel_x+1)]-sums[(nx+1+8)*pixel_y+pixel_x]);
		}
		//Put infinite values on padding on the right even though I'm doing twice for almost all rows
		for(int pixel_x=nx+1;pixel_x<nx+1+8;++pixel_x){
			sums[(pixel_y)*(nx+1+8)+pixel_x]=top_error;
			sums[(pixel_y+1)*(nx+1+8)+pixel_x]=top_error;
		}
	}
	
	//Time to do heavy computation
	#pragma omp parallel
	{ 
		float local_error=top_error; //Local error for each thread
		//Final positions and values of best rectangle found by thread
		int final_y1=0; 
		int final_x1=0;
		int final_y0=0;
		int final_x0=0;
		float final_internal_values = 0.0;
		float final_external_values = 0.0;
		//This is the bottom right sum of all the picture, we are going to access this guy, a lot, better to keep it precomputated
		float total=sums[(nx+1+8)*ny+nx];
		//Time to do loops, first: draw rectangle, then, we move it around all possible positions 
		#pragma omp for nowait schedule(dynamic,1) 
		for(int height=1;height<=ny;++height){
			for(int width=1;width<=nx;++width){
				//Get as much info of the current rectangle before moving it around
				int rectangle_pixels=height*width;
				float rectangle_pixels_2=1.0; //Auxiliar for the division
				int rest_pixels=total_pixels-rectangle_pixels; //The rest
				float rest_pixels_2=1.0; //Auxiliar
				//Preprocess these guys to do less divisions
				if(rectangle_pixels!=0){
					rectangle_pixels_2=1.0/rectangle_pixels;
				}
				if(rest_pixels!=0){
					rest_pixels_2=1.0/rest_pixels;
				}
				//Move rectangle around
				for(int y0=1,y1=height+1;y0<=ny && y1<=ny+1;++y0,++y1){
					//We increment by eight because we are comparing 8 positions of the same window
					for(int x0=1,x1=width+1;x0<=nx && x1<=nx+1;x0+=8,x1+=8){
						//We have the rectangle, time to figure out the sum of the internal and external values of eight windows
						float8_t internal_values=float8_0;
						float8_t external_values=float8_0;
						//The idea of the internal sum is bottom_right-top_right-bottom_left+top_left
						//Internal stuff
						float8_t bottom_right=_mm256_loadu_ps(&*sums.begin()+((nx+1+8)*(y1-1)+x1-1));
						float8_t top_right=_mm256_loadu_ps(&*sums.begin()+((nx+1+8)*(y0-1)+x1-1));
						float8_t bottom_left=_mm256_loadu_ps(&*sums.begin()+((nx+1+8)*(y1-1)+x0-1));
						float8_t top_left=_mm256_loadu_ps(&*sums.begin()+((nx+1+8)*(y0-1)+x0-1));
						//Calculations
						internal_values=(bottom_right-top_right)+(top_left-bottom_left);
						external_values=total-internal_values;
					
						//Give rectangle the values, and I swap the operation to multiplication
						internal_values*=rectangle_pixels_2;
						external_values*=rest_pixels_2;

						//Now we calculate the cost of each window
						float8_t error=float8_0;
						error=(error)+((internal_values*internal_values)*(-1)*float(rectangle_pixels))+((external_values*external_values)*(-1)*float(rest_pixels));
						
						//Find best among the eight if better than local found
						for(int i=0;i<8;++i){
							if(error[i]<local_error){
								local_error=error[i];
								final_y1=y1-1;
								final_x1=x1+i-1;
								final_y0=y0-1;
								final_x0=x0+i-1;
								final_internal_values=internal_values[i];
								final_external_values=external_values[i];
							}
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
				for(int c=0;c<3;++c){
					result.inner[c]=final_internal_values;
					result.outer[c]=final_external_values;
				}
			
			}	
		}
	
	}
	//End parallel
	 
	//And return
	return result;
}
