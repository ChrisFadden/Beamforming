#ifndef H5IO_H
#define H5IO_H

#include <armadillo>

namespace h5IO{
	void inputMat(const char*,const char*,arma::Mat<double> &);
}

#endif
