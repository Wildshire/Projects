/*
This is the function you need to implement. Quick reference:
- input rows: 0 <= y < ny
- input columns: 0 <= x < nx
- element at row y and column x is stored in data[x + y*nx]
- correlation between rows i and row j has to be stored in result[i + j*ny]
- only parts with 0 <= j <= i < ny need to be filled
*/
//Let's see if this works
#include <math.h>
#include <stdio.h>
void correlate(int ny, int nx, const float *data, float *result) {
	//Auxiliary variables
	//For looping
	int row1; //This is for the main row
	int row2; //This is for the rest of the rows
	int column; //Variable for going though the colum while comparing both rows
	//For storing results
	double sum1; //Sum of elements first row
	double sum2; //Sum of elements second row
	double sumPairs; //Sum of multiplied pairs
	double sumsq1; //Sum of squared elements first row
	double sumsq2; //Sum of squared elements second row
	double element1; //Element in row1
	double element2; //Element in row2
	double upper; //Upper value of fraction
	double lower; //Lower value of fraction
	double pearson_coeff; //The pearson coefficient to store
	for(row1=0;row1<ny;row1++){
		//Start at current row
		for(row2=row1;row2<ny;row2++){
			//We  want to compare two rows at the same time
			//Reseting all storing variables
			sum1=0.0d;
			sum2=0.0d;
			sumPairs=0.0d;
			sumsq1=0.0d;
			sumsq2=0.0d;
			for(column=0;column<nx;column++){
				//Get elements
				element1=data[column+row1*nx];
				element2=data[column+row2*nx];
				//Store them 
				sum1+=element1;
				sum2+=element2;
				sumPairs+=(element1*element2);
				sumsq1+=pow(element1,2.0d);
				sumsq2+=pow(element2,2.0d);
			}
			//Store result
			pearson_coeff=0.0d;
			upper=(nx*sumPairs)-(sum1*sum2);
			lower=sqrt(((nx*sumsq1)-pow(sum1,2.0d))*((nx*sumsq2)-pow(sum2,2.0d)));
			if(lower!=0.0d){
				pearson_coeff=upper/lower;
			}
			//Take advantage of symetry
			result[row1+row2*ny]=pearson_coeff;
			result[row2+row1*ny]=pearson_coeff;
		}
	}
}
