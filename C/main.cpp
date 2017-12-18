#include "armadillo"
#include "hdf5.h"
#include "pogs/matrix/matrix_dense.h"
#include "pogs/pogs.h"
#include "pogs/timer.h"
#include <iostream>

template <typename T> double LpIneq(size_t m, size_t n);

int main(int arg, char **argv) {

  /***************************
   * HDF5
   **************************/
  hid_t file_id, dataset_id, dataspace_id;
  hsize_t dims[2];
  herr_t status;

  // Create file
  file_id = H5Fcreate("test.h5", H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

  // Create Data Space
  dims[0] = 4;
  dims[1] = 6;
  dataspace_id = H5Screate_simple(2, dims, NULL);

  // Create Data Set
  dataset_id = H5Dcreate2(file_id, "/dset", H5T_STD_I32BE, dataspace_id,
			  H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);

  // Close Data Set
  status = H5Dclose(dataset_id);

  // Close Data Space
  status = H5Sclose(dataspace_id);

  // Close File
  status = H5Fclose(file_id);

  /*****************************
   *	Armadillo (Linear Algebra)
   ****************************/
  std::cout << "Armadillo version: " << arma::arma_version::as_string()
	    << std::endl;

  /*****************************
   *	POGS (Convex Optimization)
   ****************************/
  double t = LpIneq<float>(1000, 200);

  std::cout << "Hello World" << std::endl;

  return 0;
}

// Linear program in inequality form.
//   minimize    c^T * x
//   subject to  Ax <= b.
//
// See <pogs>/matlab/examples/lp_ineq.m for detailed description.
template <typename T> double LpIneq(size_t m, size_t n) {
  std::vector<T> A(m * n);

  std::default_random_engine generator;
  std::uniform_real_distribution<T> u_dist(static_cast<T>(0),
					   static_cast<T>(1));
  // Generate A according to:
  //   A = [-1 / n *rand(m - n, n); -eye(n)]
  for (unsigned int i = 0; i < (m - n) * n; ++i)
    A[i] = -static_cast<T>(1) / static_cast<T>(n) * u_dist(generator);
  for (unsigned int i = static_cast<unsigned int>((m - n) * n); i < m * n; ++i)
    A[i] = (i - (m - n) * n) % (n + 1) == 0 ? -1 : 0;

  pogs::MatrixDense<T> A_('r', m, n, A.data());
  pogs::PogsDirect<T, pogs::MatrixDense<T>> pogs_data(A_);
  std::vector<FunctionObj<T>> f;
  std::vector<FunctionObj<T>> g;

  // Generate b according to:
  //   b = A * rand(n, 1) + 0.2 * rand(m, 1)
  f.reserve(m);
  for (unsigned int i = 0; i < m; ++i) {
    T b_i = static_cast<T>(0);
    for (unsigned int j = 0; j < n; ++j)
      b_i += A[i * n + j] * u_dist(generator);
    b_i += static_cast<T>(0.2) * u_dist(generator);
    f.emplace_back(kIndLe0, static_cast<T>(1), b_i);
  }

  // Generate c according to:
  //   c = rand(n, 1)
  g.reserve(n);
  for (unsigned int i = 0; i < n; ++i)
    g.emplace_back(kIdentity, u_dist(generator) / n);

  double t = timer<double>();
  pogs_data.Solve(f, g);

  return timer<double>() - t;
}
