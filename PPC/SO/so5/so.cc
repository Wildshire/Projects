#include <algorithm>
#include <vector>
#include <iostream>
#include <iterator>
#include <numeric>
#include <omp.h>
#include <bits/stdc++.h> 

typedef unsigned long long data_t;

constexpr long long sort=4194304;
//constexpr long long split=16777216;
//Auxiliar functions

//Recursive function, it has both secuential an parallel versions
void quicksort(data_t *iBegin,  data_t *iEnd){
	//Consider it sorted
	if(iBegin>=iEnd){
        	return;
	}
	//Go for sorting if few elements
	//printf("Partition Lenght: %ld\n",iEnd - iBegin);
	if(iEnd - iBegin<=sort){
		std::sort(iBegin,iEnd);
	}
	//Go parallel
	else{
		//Geting median and place it on correct pos
		data_t *iMiddle=std::next(iBegin, std::distance(iBegin,iEnd)/2);;
		//Place pivot
		std::nth_element(iBegin,iMiddle,iEnd);
		
		//Do the partitions now, I used implementation in std::partition example
		unsigned long long pivot = *(iMiddle);
    		data_t * middle1 = std::partition(iBegin, iMiddle, [pivot](const data_t em){ return em < pivot; });
    		data_t * middle2 = std::partition(middle1, iEnd, [pivot](const data_t em){ return !(pivot < em); });
		//Parallel version
		//These two things are independent to each other
			#pragma omp task shared (iBegin,middle1)
			{	//printf("Thread ID: %d\n",omp_get_thread_num());
				quicksort(iBegin, middle1);  // sort the left  run
			}
			#pragma omp task shared (middle2,iEnd)
			{	//printf("Thread ID: %d\n",omp_get_thread_num());
				quicksort(middle2,iEnd);  // sort the right run
		
			}
		
		
	}


}


//Same as SO4
void psort(int n, data_t *data) {
    // Implement a more efficient parallel sorting algorithm for the CPU,
    // using the basic idea of quicksort.
	data_t *first=data;
	data_t *end=data+n;
	#pragma omp parallel shared (first,end,n)
	{
		#pragma omp single 
		{
		quicksort(first,end);
		}
	//#pragma omp taskwait
	}
}
