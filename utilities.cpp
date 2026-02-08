#include "utilities.h"

int incrementByValueNumTimes(int startValue, int increment, int numTimes)
{
	for (int i = 0; i < numTimes; i++)
		startValue += increment;

	return startValue;
}

// BEGIN: 1d
///*returverdi*/ incrementByValueNumTimesRef(/*param 1: startValue(ref), param 2: increment, param 3: numTimes*/){}
// END: 1d

// BEGIN: 1e
///*returverdi*/ swapNumbers(/*parametre*/){}
// END: 1e

// BEGIN: 2b
///*returverdi*/ printStudent(/*input Student*/) {}
// END: 2b

// BEGIN: 2c
///*returverdi*/ isInProgram(/*param 1: Student, param 2: string*/){}
// END: 2c


// BEGIN: 3a
///*returverdi*/ randomizeString(/*param 1: antall tegn, param 2: øvre grense, param 3: nedre grense */) 
// END: 3a

// BEGIN: 3c
///*returverdi*/ readInputToString(/*param 1: lengde n, param 2: øvre grense, param 3: nedre grense*/)
// END: 3c

// BEGIN: 3d
///*returverdi*/ countChar(/*param 1: string, param 2: char*/)
// END: 3d
