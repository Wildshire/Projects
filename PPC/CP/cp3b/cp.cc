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
typedef float float8_t __attribute__ ((vector_size (8*sizeof(float))));

//Creating pointer of vectors alligning with memory, book example
float8_t * float8_alloc(std::size_t n){
	void * tmp=0;
	if(posix_memalign(&tmp,sizeof(float8_t),sizeof(float8_t)*n)){
		throw std::bad_alloc();
	}
	return (float8_t *) tmp;
}


void correlate(int ny, int nx, const float *data, float *result) {

	//Preparations of column registers
	constexpr int nb = 8;
	int na=(nx+nb-1)/nb;

	//Preparations of row blocks 8*8 window
	constexpr int nd = 8;
	int nc = (ny+nd-1)/nd;
	int ncd = nc*nd;

	float8_t *x = float8_alloc(ncd*na);

	float8_t float8_0 = {0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};

	//Now x  will cointain data mean and std normalized
	//Same initialization as cp2b
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ncd;++row){
		for (int ka=0;ka<na;++ka){
			for(int kb=0;kb<nb;++kb){
				int column=ka*nb+kb;
				//If column < nx and row < ny then yeah, we do not want segmentation fault or similar
				if(column<nx && row<ny){
					x[row*na+ka][kb] = data[column + row*nx];
				}
				else{
				 	x[row*na+ka][kb] = 0.0;
				}
			}
		}
		//We do not want 0/0
		if(row<ny){
			//Mean
			float8_t sum=float8_0;
			float aux=0.0;
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
			float8_t sum2=float8_0;
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
	}
	//Multiplication
	//Store results here by multiplying elements
	asm("##########MATRIX MULTIPLICATION LOOP##########");
	#pragma omp parallel for schedule(dynamic,1)
	for(int ic=0;ic<nc;++ic){
		for(int jc=ic;jc<nc;++jc){
			//Matrix of pearsons coefficients
			float8_t v_pearson_coeff[nd][nd];
			for(int id=0;id<nd;++id){
				for(int jd=0;jd<nd;++jd){
					v_pearson_coeff[id][jd]=float8_0;
				}
			}
			//Multply registers and sum them up
			float8_t first[nd];
			float8_t second[nd];
			for(int ka=0;ka<na;++ka){
				for(int id=0;id<nd;++id){
					//First block
					first[id]=x[na*(ic*nd+id)+ka];
					//Second block
					second[id]=x[na*(jc*nd+id)+ka];
				}
				//Multiplication
				for(int id=0;id<nd;++id){
					for(int jd=0;jd<nd;++jd){
						v_pearson_coeff[id][jd]+=first[id]*second[jd];
					}
				}

			}
					
			//Sum them up
			for(int id=0;id<nd;++id){
				for(int jd=0;jd<nd;++jd){
					float8_t aux_pearson_coeff=v_pearson_coeff[id][jd];
					float pearson_coeff=0.0;
					for(int kb=0;kb<nb;++kb){
						pearson_coeff+=aux_pearson_coeff[kb];
					}
					//We have symetry
					int row=ic*nd+id;
					int row_aux=jc*nd+jd;
					if(row<ny && row_aux<ny){
						result[row+row_aux*ny]=pearson_coeff;
						result[row_aux+row*ny]=pearson_coeff;
					}
				}
			}
			
		}
	}
	//Free x
	std::free(x);
	
}

