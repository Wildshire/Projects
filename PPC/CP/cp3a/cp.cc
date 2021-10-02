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
#include <tuple>
#include <x86intrin.h>

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
	//
	double result_2[ny][ny]={ };
	//Debugging 
	//int debug=1;

	//Preparations of column vectors
	constexpr int nb = 4;
	int na=(nx+nb-1)/nb;

	//Preparation for column blocks, we do not want to read all the row in one shot
	constexpr int nb_2=20;
	int na_2=(na+nb_2-1)/nb_2;

	//Preparations of row blocks
	constexpr int nd = 8;
	int nc = (ny+nd-1)/nd;
	int ncd = nc*nd;

	//With out column blocks
	//int index=na;
	//double4_t *x = double4_alloc(ncd*na);
	//with column blocks
	int index=nb_2*na_2;
	double4_t *x = double4_alloc(ncd*nb_2*na_2);

	//Auxiliary initialization
	double4_t double4_0={0.0,0.0,0.0,0.0};
	
	//New indexes
	std::vector<std::tuple<int,int,int>> rows(nc*nc);
	
	//#pragma omp parallel for schedule(dynamic,1)
	for (int ic = 0; ic < nc; ++ic) {
    		for (int jc = 0; jc < nc; ++jc) {
        		int ijc = _pdep_u32(ic, 0x55555555) | _pdep_u32(jc, 0xAAAAAAAA);
        		rows[ic*nc + jc] = std::make_tuple(ijc, ic, jc);
    		}
	}
	
	std::sort(rows.begin(), rows.end());

	//Now x will cointain data mean and std normalized
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ncd;++row){
		for(int ka=0;ka<na;++ka){
			for(int kb=0;kb<nb;++kb){
				int column=ka*nb+kb;
				//If column < nx and row < ny then yeah, we do not want segmentation fault or similar
				if(column<nx && row<ny){
					x[row*index+ka][kb] = double(data[column + row*nx]);
				}
				else{
				 	x[row*index+ka][kb] = 0.0;
				}
			}	
		}
		//We do not want 0/0
		if(row<ny){
			//Mean
			double4_t sum=double4_0;
			double aux=0.0;
			for(int ka=0; ka<na-1; ka=ka+2){
				sum+=x[row*index + ka]+x[row*index + ka+1];
			}
			//Last register
			int odd = na%2;
			if(odd==1){
				sum+=x[row*index+(na-1)];
			}
			//Sum the 4 elements of all the sums
			for(int kb=0;kb<nb;++kb){
				aux+=double(sum[kb]);
			}
			//This is the mean
			aux=double(aux/nx);
			//Substract to every register
			for(int ka=0;ka<na;++ka){
				x[row*index+ka]=x[row*index+ka]-aux;
			}
		
			//Check zeros last register not to contaminate the norm
			for(int kb=0;kb<nb;++kb){
				int column=(na-1)*nb+kb;
				x[row*index+(na-1)][kb] = column < nx ? double(x[row*index+(na-1)][kb]) : 0.0;
			}
		
			//Norm
			double4_t sum2=double4_0;
			aux=0.0;
			for(int ka=0;ka<na-1;ka=ka+2){
				sum2+=x[row*index+ka]*x[row*index+ka]+x[row*index+ka+1]*x[row*index+ka+1];
			}
			//Last resgister
			if(odd==1){
				sum2+=x[row*index+(na-1)]*x[row*index+(na-1)];
			}
			//Sum the 4 elements of all the sums
			for (int kb=0;kb<nb;++kb){
				aux+=double(sum2[kb]);
			}
			//This is the norm
			aux=double(sqrt(aux));
			//Divide to each register
			for(int ka=0;ka<na;++ka){
				x[row*index+ka]=x[row*index+ka]/aux;
			}
		}
	}
	//Multiplication
	//Store results here by multiplying elements
	asm("##########MATRIX MULTIPLICATION LOOP##########");
	#pragma omp parallel for schedule(dynamic,1)
	for(int ka_1=0;ka_1<nb_2;++ka_1){
		for(int ka_2=0;ka_2<na_2;++ka_2){
			int ka=ka_1*na_2+ka_2;
			//Matrix of pearsons coefficients
			double4_t v_pearson_coeff[nd][nd];
			for(int id=0;id<nd;++id){
				for(int jd=0;jd<nd;++jd){
					v_pearson_coeff[id][jd]=double4_0;
				}
			}
			//Multply registers and sum them up
			double4_t first[nd];
			double4_t second[nd];
			
			//double pearson_coeffs[nc*nc];
			for(int row_col=0;row_col<nc*nc;++row_col){
				int ic=std::get<1>(rows[row_col]);
				int jc=std::get<2>(rows[row_col]);
				for(int id=0;id<nd;++id){
					//First block
					first[id]=x[index*(ic*nd+id)+ka];
					//Second block
					second[id]=x[index*(jc*nd+id)+ka];
				}
				for(int id=0;id<nd;++id){
					for(int jd=0;jd<nd;++jd){
						//#pragma omp critical
						v_pearson_coeff[id][jd]=first[id]*second[jd];
					}
				}

				for(int id=0;id<nd;++id){
					for(int jd=0;jd<nd;++jd){
						double4_t aux_pearson_coeff=v_pearson_coeff[id][jd];
						double pearson_coeff=0.0;
						for(int kb=0;kb<nb;++kb){
							pearson_coeff+=double(aux_pearson_coeff[kb]);
						}
						//We have symetry
						int row=ic*nd+id;
						int row_aux=jc*nd+jd;
						#pragma omp critical
						if(row<ny && row_aux<ny){
							//result[row+row_aux*ny]+=pearson_coeff;
							//result[row_aux+row*ny]+=pearson_coeff;
							result_2[row][row_aux]+=pearson_coeff;
						}
					}
				}
			}
		}
	}
	//Copy to result
	#pragma omp parallel for schedule(dynamic,1)
	for(int row=0;row<ny;++row){
		for(int row_aux=row;row_aux<ny;++row_aux){
		result[row+row_aux*ny]=result_2[row][row_aux];
		result[row_aux+row*ny]=result_2[row][row_aux];
		}
	}
	//Free x
	std::free(x);
	
}


