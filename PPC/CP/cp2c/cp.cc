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


void correlate(int ny, int nx, const float *data, float *result) {

	//Preparations of the vectors
	constexpr int nb = 4;
	int na=(nx+nb-1)/nb;
	double4_t * x = double4_alloc(ny*na);

	//Now x and x_t will cointain data mean and std normalized
	for(int row=0;row<ny;++row){
		for (int ka=0;ka<na;++ka){
			for(int kb=0;kb<nb;++kb){
				int column=ka*nb+kb;
				//If column < nx then yeah, we do not want segmentation fault ror similar
				x[row*na+ka][kb] = column < nx ? data[column + row*nx] : 0.0;
				//printf("%f \n",x[row*na+ka][kb]);
			}
		}
		//Mean
		double4_t sum={0.0,0.0,0.0,0.0};
		double aux=0.0;
		for(int ka=0; ka<na-1; ka=ka+2){
			sum+=x[row*na + ka]+x[row*na + ka+1];
		}
		//Last register
		int odd = na%2;
		if(odd==1){
			sum+=x[row*na+(na-1)];
		}
		//Sum the 4 elements of all the sums
		for(int kb=0;kb<nb;++kb){
			aux+=sum[kb];
		}
		//This is the mean
		aux=aux/nx;
		//Substract to every register
		for(int ka=0;ka<na;++ka){
			x[row*na+ka]=x[row*na+ka]-aux;
		}
		
		//Check zeros last register not to contaminate the norm
		for(int kb=0;kb<nb;++kb){
			int column=(na-1)*nb+kb;
			x[row*na+(na-1)][kb] = column < nx ? x[row*na+(na-1)][kb] : 0.0;
		}
		
		//Norm
		double4_t sum2={0.0,0.0,0.0,0.0};
		aux=0.0;
		for(int ka=0;ka<na-1;ka=ka+2){
			sum2+=x[row*na+ka]*x[row*na+ka]+x[row*na+ka+1]*x[row*na+ka+1];
		}
		//Last resgister
		if(odd==1){
			sum2+=x[row*na+(na-1)]*x[row*na+(na-1)];
		}
		//Sum the 4 elements of all the sums
		for (int kb=0;kb<nb;++kb){
			aux+=sum2[kb];
		}
		//This is the norm
		aux=sqrt(aux);
		//Divide to each register
		for(int ka=0;ka<na;++ka){
			x[row*na+ka]=x[row*na+ka]/aux;
		}
	}
	//Multiplication
	//Store results here by multiplying elements
	for(int row=0;row<ny;++row){
		for(int row_aux=row;row_aux<ny;++row_aux){
			//Vector
			double4_t v_pearson_coeff={0.0,0.0,0.0,0.0};
			//Multply registers and sum them up
			for(int ka=0;ka<na;++ka){
				double4_t first=x[row*na+ka];
				double4_t second=x[row_aux*na+ka];
				v_pearson_coeff+=(first*second);
			}
	
			//Sum them up
			double pearson_coeff=0.0;
			for(int kb=0;kb<nb;++kb){
				pearson_coeff+=v_pearson_coeff[kb];
			}
			//We have symetry
			result[row+row_aux*ny]=pearson_coeff;
			result[row_aux+row*ny]=pearson_coeff;
		}
	}
	//Free x
	std::free(x);
	
}
