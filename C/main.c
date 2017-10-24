#include "cblas.h"
#include "ecos.h"
#include "hdf5.h"
#include "lapacke.h"
#include <stdio.h>
#include <stdlib.h>

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

  /*******************************
   * BLAS / LAPACK
   ******************************/

  double A_BLAS[2] = {0.0, 0.0}, B[2] = {0.0, 0.0}, C[2] = {0.0, 0.0},
	 ALPHA = 0.0, BETA = 0.0;

  cblas_dgemm(CblasRowMajor, CblasTrans, CblasNoTrans, 1, 0, 0, ALPHA, A_BLAS,
	      1, B, 1, BETA, C, 1);

  lapack_int n, nrhs, lda, ldb, info;
  int i, j;
  /* Local arrays */
  double *A, *b;
  lapack_int *ipiv;

  n = 5;
  nrhs = 1;
  lda = n, ldb = 5;
  A = (double *)malloc(n * n * sizeof(double));
  b = (double *)malloc(n * nrhs * sizeof(double));
  ipiv = (lapack_int *)malloc(n * sizeof(lapack_int));
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++)
      A[i * lda + j] = ((double)rand()) / ((double)RAND_MAX) - 0.5;
  }

  for (i = 0; i < n * nrhs; i++)
    b[i] = ((double)rand()) / ((double)RAND_MAX) - 0.5;

  dgesv_(&n, &nrhs, A, &lda, ipiv, b, &ldb, &info);

  /*******************************
   *	ECOS
   ******************************/
  pwork *mywork;

  printf("Hello World\n");

  return 0;
}
