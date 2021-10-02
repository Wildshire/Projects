/*
This is the function you need to implement. Quick reference:
- input rows: 0 <= y < ny
- input columns: 0 <= x < nx
- element at row y and column x is stored in data[x + y*nx]
- correlation between rows i and row j has to be stored in result[i + j*ny]
- only parts with 0 <= j <= i < ny need to be filled
*/

//THIS IS MY VERSION OF CP2B, TOOK PREPROCESSING PART

//Imports
#include <stdio.h>
#include <vector>
#include <math.h>
#include <typeinfo>
#include <algorithm>

#include <cstdlib>
#include <iostream>
#include <cuda_runtime.h>

//constexpr int rounding=8;

//GPU auxiliary functions
static inline void check(cudaError_t err, const char* context) {
    if (err != cudaSuccess) {
        std::cerr << "CUDA error: " << context << ": "
            << cudaGetErrorString(err) << std::endl;
        std::exit(EXIT_FAILURE);
    }
}

#define CHECK(x) check(x, #x)

static inline int divup(int a, int b) {
    return (a + b - 1)/b;
}

static inline int roundup(int a, int b) {
    return divup(a, b) * b;
}

//GPU padding kernel
__global__ void paddingkernel(float* copy_x, float* divisions, float* x, float* result, int nx, int nn_x, int ny) {
	//Get thread info
	int ja = threadIdx.x;
	int row = blockIdx.y;
	
	//Transfer padded values to x
    	for (int jb = 0; jb < nn_x; jb+=64) {
		int column=ja+jb;
		float value=0.0;
		if(row<ny && column < nx){
			value=copy_x[row*nx + column]/sqrt(divisions[row]);
		}
		x[row*nn_x + column] = value;
    	}
	//Initialize result
	for(int column=0;column<ny;++column){
		if(row<ny){
			result[row*ny+column]=0.0;
		}
	}
}

//GPU main kernel 

__global__ void mykernel(float* x,float* result, int nx, int nn_x, int ny, int nn_y) {
	int ia = threadIdx.x; 
    	int ja = threadIdx.y; 
    	int ic = blockIdx.x; 
    	int jc = blockIdx.y;

	__shared__ float firsts[4][64];
    	__shared__ float seconds[4][64]; 

	//Initialization
	float pearson_coeff[8][8];
    	for (int ib = 0; ib < 8; ++ib) {
        	for (int jb = 0; jb < 8; ++jb) {
            		pearson_coeff[ib][jb] = 0.0;
        	}
    	}
	
	//Do the calculation
	for (int ks = 0; ks < nn_x; ks += 4) {
		int col=ia*8+ja;
            	int row = ic * 64 + col;
		int row_aux = jc * 64 + col;
		for (int f = 0; f < 4; ++f) {
            		int k = ks + f;
            		firsts[f][col] = x[nn_x*row + k];
            		seconds[f][col] = x[nn_x*row_aux + k];
        	}
			
		__syncthreads();
		
        	//Multiplication
		#pragma unroll
        	for (int f = 0; f < 4; ++f) {
            		float second[8]={0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};
			for (int jb = 0; jb < 8; ++jb) {
                		second[jb] = seconds[f][jb * 8 + ja];
            		}
            		for (int ib = 0; ib < 8; ++ib) {
                		float first = firsts[f][ib * 8 + ia];
                		for (int jb = 0; jb < 8; ++jb) {
                			pearson_coeff[ib][jb] += first*second[jb];
            			}
        		}
		}
	
		 __syncthreads();

	}
	for (int ib = 0; ib < 8; ++ib) {
        	for (int jb = 0; jb < 8; ++jb) {
         		int row = ic * 64 + ib * 8 + ia;
            		int row_aux = jc * 64 + jb * 8 + ja;
			if (row < ny && row_aux < ny) {
                		result[ny*row_aux + row] += pearson_coeff[ib][jb];
				//result[ny*row_aux + row] += pearson_coeff[ib][jb];
            		}
        	}
    	}
	
}

//CPU auxiliary functions
//Struct for sum
struct Sum{
	auto operator() (float n){ sum +=n; }
	float sum{0};
};


//Struc for square_sum
struct Square_sum{
	auto operator() (float n){ sq_sum += pow(n,2.0f); }
	float sq_sum{0};
};

void correlate(int ny, int nx, const float *data, float *result) {
	//asm("CPU PART I");
	//Auxiliary variables
	std::vector <float> x(ny*nx,0.0); //x matrix
	std::vector <float> divisions(ny,0.0); //Store the divisions we are going to do in cuda

	//Now x will cointain data mean and std normalized
	for(int row=0;row<ny;++row){
		for (int column=0;column<nx;++column){
			x[column + row*nx]=data[column + row*nx];
		}
		//Mean
		//Sum all values
		Sum s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Sum());
		//Substract mean to all of them
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (float &n){n=n-(s.sum/nx);});

		//Norm
		Square_sum sq_s = std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),Square_sum());
		//Store division
		//std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (float &n){n=n/sqrt(sq_s.sq_sum);});
		divisions[row]=sq_s.sq_sum;
	}

	//asm("GPU PART");
	int nn_x = roundup(nx, 64);
	int nn_y = roundup(ny, 64);
	//Memory storing
	float* xGPU=NULL; //This one will be padded
	CHECK(cudaMalloc((void**)&xGPU, nn_y * nn_x * sizeof(float)));
	
	float* copy_xGPU = NULL; //This one will get the data
    	CHECK(cudaMalloc((void**)&copy_xGPU, ny * nx * sizeof(float)));
    	CHECK(cudaMemcpy(copy_xGPU, &*x.begin(), ny * nx * sizeof(float), cudaMemcpyHostToDevice));
	
	float* copy_divisions = NULL; //This one will get the divisions for each row
    	CHECK(cudaMalloc((void**)&copy_divisions, ny * sizeof(float)));
    	CHECK(cudaMemcpy(copy_divisions, &*divisions.begin(), ny * sizeof(float), cudaMemcpyHostToDevice));
		
	//Preparations for calulation
	float* resultGPU = NULL;
    	CHECK(cudaMalloc((void**)&resultGPU, ny * ny * sizeof(float)));
	// Divisions, padding and initialization
    	{
        	dim3 dimBlock(64, 1);
        	dim3 dimGrid(1, nn_y);
        	paddingkernel<<<dimGrid, dimBlock>>>(copy_xGPU, copy_divisions,xGPU, resultGPU, nx, nn_x, ny);
        	CHECK(cudaGetLastError());
    	}

	
    	// Run calculations kernel
	{
		dim3 dimBlock(8, 8);
        	dim3 dimGrid(nn_y / 64, nn_y / 64);
    		mykernel<<<dimGrid, dimBlock>>>(xGPU, resultGPU, nx, nn_x, ny, nn_y);
    		CHECK(cudaGetLastError());
	}

    	// Copy data back to CPU & release memory
    	CHECK(cudaMemcpy(result, resultGPU, ny * ny * sizeof(float), cudaMemcpyDeviceToHost));
    	CHECK(cudaFree(copy_divisions));
	CHECK(cudaFree(copy_xGPU));
	CHECK(cudaFree(xGPU));
    	CHECK(cudaFree(resultGPU));
}

