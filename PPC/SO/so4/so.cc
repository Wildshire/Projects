#include <algorithm>
#include <vector>
#include <iostream>
#include <iterator>
#include <numeric>
#include <omp.h>
#include <bits/stdc++.h> 

typedef unsigned long long data_t;

constexpr int limit=16384;

//Auxiliar functions

//Recursive function, it has both secuential an parallel versions
void TopDownSplitMerge(data_t *A, int iBegin, int iEnd){
	//If size 1, consider it sorted
	if(iEnd - iBegin <= 1){
        	return;
	}
	// Get pointer to half
	int iMiddle = (iEnd + iBegin) / 2;
	//If we have few elements do sort, if not, parallel
	if(iEnd - iBegin<=limit){
		std::sort(A+iBegin,A+iEnd);
	}
	//Parallel version
	else{
			#pragma omp taskgroup
			{	
				//These two things are independent to each other
				#pragma omp task shared(A,iBegin,iMiddle) if (omp_get_num_threads()>1)
				{
					TopDownSplitMerge(A, iBegin, iMiddle);  // sort the left  run
				}
				 #pragma omp task shared(A,iBegin,iMiddle) if (omp_get_num_threads()>1)
				{
					TopDownSplitMerge(A, iMiddle, iEnd);  // sort the right run
				}
				//#pragma omp taskyield
			}
			std::inplace_merge(A+iBegin, A+iMiddle, A+iEnd); //And merge
	}
}

// Implement a more efficient parallel sorting algorithm for the CPU,
// using the basic idea of merge sort.
void psort(int n, data_t *data) {
	
	//Call aux function
	#pragma omp parallel
	{
		#pragma omp single
		{
			TopDownSplitMerge(data,0,n);
		}
	}

}
