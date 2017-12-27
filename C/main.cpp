#include "armadillo"
#include "hdf5.h"
#include "pogs/matrix/matrix_dense.h"
#include "pogs/pogs.h"
#include "pogs/timer.h"
#include "h5IO.h"
#include <iostream>


#define FP	"../../build/ULA.h5"

int main(int arg, char **argv) {
	
	/***********************
	 * Simulation Parameters
	 **********************/
			
	/********************
	 * Read in Matrix
	 *******************/
	arma::Mat<double> B;
	h5IO::inputMat(FP,"/Phase",B);
	
  std::cout << "Hello World" << std::endl;

  return 0;
}


