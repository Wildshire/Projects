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
	int row; //This is for indexing
	int column; //This is indexing
	int row_aux; //Aux for x*x_transpose
	double first;
	double second;
	double pearson_coeff;
	//std::vector <float> data_t(ny*nx);
	std::vector <double> x(ny*nx); //x matrix
	//std::vector <double> x_t(ny*nx); //x transpose
	
	//First create transpose of data
	/*for(row=0;row<ny;row++){
		for(column=0;column<nx;column++){
			data_t[row + column*nx]=data[column + row*nx];
		}
	}*/

	//Now x and x_t will cointain data mean and std normalized
	for(row=0;row<ny;row++){
		for (column=0;column<nx;column++){
			x[column + row*nx]=data[column + row*nx];
			//x_t[column + row*nx]=data_t[column + row*nx];
		}
		//Mean
		//Sum all values
		Sum s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Sum());
		//Substract mean to all of them
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (double &n){n=n-(s.sum/nx);});

		//Std
		Square_sum sq_s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Square_sum());
		//Divide norm
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (double &n){n=n/sqrt(sq_s.sq_sum);});

	}
	//Store results here by multiplying elements
	for(row=0;row<ny;row++){
		for(row_aux=row;row_aux<ny;row_aux++){
			pearson_coeff=0.0d;
			for(column=0;column<nx;column++){
				//We have symetry
				first=x[column+row*nx];
				second=x[column+row_aux*nx];
				pearson_coeff+=first*second;
			}
			result[row+row_aux*ny]=pearson_coeff;
			result[row_aux+row*ny]=pearson_coeff;
		}
	}
	
}
