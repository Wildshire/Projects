/*
This is the function you need to implement. Quick reference:
- input rows: 0 <= y < ny
- input columns: 0 <= x < nx
- element at row y and column x is stored in data[x + y*nx]
- correlation between rows i and row j has to be stored in result[i + j*ny]
- only parts with 0 <= j <= i < ny need to be filled
*/

//Imports
#include <stdio.h>
#include <vector>
#include <math.h>
#include <typeinfo>
//Struct for sum
struct Sum{
	auto operator() (double n){ sum +=n; }
	double sum{0};
};


//Struc for square_sum
struct Square_sum{
	auto operator() (double n){ sq_sum += pow(n,2.0f); }
	double sq_sum{0};
};

void correlate(int ny, int nx, const float *data, float *result) {
	//Auxiliary variables
	
	std::vector <double> x(ny*nx,0.0); //x matrix

	//Now x and x_t will cointain data mean and std normalized
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ny;++row){
		//This is for sure can be parallelised
		for (int column=0;column<nx;++column){
			x[column + row*nx]=data[column + row*nx];
		}
		//Mean
		//Sum all values
		Sum s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Sum());
		//Substract mean to all of them
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (double &n){n=n-(s.sum/nx);});

		//Norm
		Square_sum sq_s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Square_sum());
		//Divide norm
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (double &n){n=n/sqrt(sq_s.sq_sum);});
	}

	//Store results here by multiplying elements
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ny;++row){
		for(int row_aux=row;row_aux<ny;++row_aux){
			double pearson_coeff=0.0;
			for(int column=0;column<nx;++column){
				double first=x[column+row*nx];
				double second=x[column+row_aux*nx];
				pearson_coeff+=first*second;
			}
			result[row+row_aux*ny]=pearson_coeff;
			result[row_aux+row*ny]=pearson_coeff;
		}
	}
}
