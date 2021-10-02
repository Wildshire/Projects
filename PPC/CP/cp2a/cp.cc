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
	auto operator() (double n){ sq_sum += n*n; }
	double sq_sum{0};
};

void correlate(int ny, int nx, const float *data, float *result) {
	//Auxiliary variables
	int row; //This is for indexing
	int column; //This is indexing
	int row_aux; //Aux for x*x_transpose
	
	//Same as class
	constexpr int nb = 4;
	int na = (nx+nb-1)/nb;
	int nab=na*nb;
	std::vector <double> x(ny*nab,0.0); //x matrix


	//Now x  will cointain data mean and std normalized
	for(row=0;row<ny;row++){
		for (column=0;column<nx;column++){
			x[column + row*nab]=data[column + row*nx];
		}
		//Mean
		//Sum all values
		Sum s = std::for_each(x.begin()+(row*nab),x.begin()+(nx+row*nab),Sum());
		//Substract mean to all of them
		std::for_each(x.begin()+(row*nab),x.begin()+(nx+row*nab),[&] (double &n){n=n-(s.sum/nx);});

		//Norm
		Square_sum sq_s = std::for_each(x.begin()+(row*nab),x.begin()+(nx+row*nab),Square_sum());
		//Divide norm
		std::for_each(x.begin()+(row*nab),x.begin()+(nx+row*nab),[&] (double &n){n=n/sqrt(sq_s.sq_sum);});

	}

	//Store results here by multiplying elements
	for(row=0;row<ny;++row){
		for(row_aux=row;row_aux<ny;++row_aux){
			//Declare vector here
			std::vector <double> v_pearson_coeff(nb);
			for(int i=0;i<nb;++i){
				v_pearson_coeff[i]=0.0;
			}
			for(int ka=0;ka<na;++ka){
				for(int kb=0;kb<nb;++kb){
					double first=x[(ka*nb+kb)+row*nab];
					double second=x[(ka*nb+kb)+row_aux*nab];
					v_pearson_coeff[kb]+=first*second;
				}
			}
			double pearson_coeff=0.0;
			for(int kb=0;kb<nb;++kb){
				pearson_coeff+=v_pearson_coeff[kb];
			}
			//Symetry
			result[row+row_aux*ny]=pearson_coeff;
			result[row_aux+row*ny]=pearson_coeff;
		}
	}
}
