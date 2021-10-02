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

//Not needed yet
//static inline int roundup(int a, int b) {
  //  return divup(a, b) * b;
//}
 

__global__ void mykernel(float* x, float* result, int nx, int ny) {
	int row_aux = threadIdx.x + blockIdx.x * blockDim.x;
    	int row = threadIdx.y + blockIdx.y * blockDim.y;
    	if (row >= ny || row_aux >= ny){
        	return;
	}
	//printf("Row: %d, Row_aux: %d, NX: %d, NY: %d\n", row,row_aux,nx,ny);
    	float pearson_coeff = 0.0;
    	for (int column = 0; column < nx; ++column) {
        	float first = x[row*nx + column];
        	float second = x[row_aux*nx + column];
		//printf("First: %f, Second: %f\n",first,second);
		pearson_coeff+=first*second;
    	}
    	result[row+row_aux*ny] = pearson_coeff;
	result[row_aux+row*ny] = pearson_coeff;
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

	//Now x will cointain data mean and std normalized
	#pragma omp parallel for schedule(dynamic,1)
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
		//Divide norm
		std::for_each(x.begin()+(row*nx),x.begin()+(nx+row*nx),[&] (float &n){n=n/sqrt(sq_s.sq_sum);});
	}

	//asm("GPU PART");
	//Memory storing
	float* xGPU = NULL;
    	CHECK(cudaMalloc((void**)&xGPU, ny * nx * sizeof(float)));
    	float* resultGPU = NULL;
    	CHECK(cudaMalloc((void**)&resultGPU, ny * ny * sizeof(float)));
    	CHECK(cudaMemcpy(xGPU, &*x.begin(), ny * nx * sizeof(float), cudaMemcpyHostToDevice));

    	// Run kernel
    	dim3 dimBlock(16, 16);
    	dim3 dimGrid(divup(ny, dimBlock.x), divup(ny, dimBlock.y));
    	mykernel<<<dimGrid, dimBlock>>>(xGPU, resultGPU, nx, ny);
    	CHECK(cudaGetLastError());

    	// Copy data back to CPU & release memory
    	CHECK(cudaMemcpy(result, resultGPU, ny * ny * sizeof(float), cudaMemcpyDeviceToHost));
    	CHECK(cudaFree(xGPU));
    	CHECK(cudaFree(resultGPU));
}
