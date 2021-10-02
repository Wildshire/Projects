#include <iostream>
#include <time.h>

//Clock function
uint64_t rdtsc(){
    unsigned int lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

int main(){
	//Preparing variables
	float a = 1.1;
	float b = 1.2;
	float result=0.0;
	//1000 mill operations
	uint64_t tick = rdtsc(); //Clock ticks
	struct timespec wall_begin, wall_end;//Wall time
	struct timespec cpu_begin, cpu_end;//CPU time 
    	clock_gettime(CLOCK_REALTIME, &wall_begin);
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &cpu_begin);
	
	//THE PROGRAM
	asm("############LOOP############");
	for(int i=0;i<1000000000;++i){
		result=result+(a-b)*(a+b)+(a+b)/(a-b);
	}
	//END OF PROGRAM

	//Measure Clock cycles
	uint64_t tick_diff = rdtsc() - tick;
	printf("Number of clock cycles: %ld\n",tick_diff);
	//Measure Wall and CPU time
	clock_gettime(CLOCK_REALTIME, &wall_end);
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &cpu_end);
    	long wallseconds = wall_end.tv_sec - wall_begin.tv_sec;
    	long cpuseconds = cpu_end.tv_sec - cpu_begin.tv_sec;
    	long wallnanoseconds = wall_end.tv_nsec - wall_begin.tv_nsec;
    	long cpunanoseconds = cpu_end.tv_nsec - cpu_begin.tv_nsec;
    	double wallelapsed = wallseconds + wallnanoseconds*1e-9;
    	double cpuelapsed = cpuseconds + cpunanoseconds*1e-9;
	printf("The program took %f seconds of wall time\n", wallelapsed);
	printf("The program took %f seconds of cpu time\n", cpuelapsed);
	

}
