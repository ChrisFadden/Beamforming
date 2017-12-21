#include "armadillo"
#include "hdf5.h"
#include "pogs/matrix/matrix_dense.h"
#include "pogs/pogs.h"
#include "pogs/timer.h"
#include <iostream>


#define FP	"../../build/ULA.h5"

int main(int arg, char **argv) {
	
	/***********************
	 * Simulation Parameters
	 **********************/
	

	/***********************
	 * Read in HDF5 file
	 **********************/	
	hid_t file_id, dataset_id;
	hid_t dataspace, datatype;
	int status_n;	
	hsize_t	dims[2] = {0, 0};
	herr_t status;	

	file_id = H5Fopen(FP,H5F_ACC_RDONLY,H5P_DEFAULT);
	dataset_id = H5Dopen2(file_id, "/listAzm",H5P_DEFAULT);

  dataspace = H5Dget_space(dataset_id);    /* dataspace handle */
  status_n  = H5Sget_simple_extent_dims(dataspace, dims, NULL);
	
	std::cout << "dimensions " << dims[0] << " x  " << dims[1] << std::endl;
	
	datatype = H5Dget_type(dataset_id); 
	
	double* dataArray = (double*) malloc(dims[0]*sizeof(double));
	
	status = H5Dread(dataset_id, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL,
		     H5P_DEFAULT, dataArray);
		
	/**********************
	 * Delete Pointers
	 *********************/
	free(dataArray);	
	status = H5Sclose(dataspace);
	status = H5Dclose(dataset_id);
  status = H5Fclose(file_id);

  std::cout << "Hello World" << std::endl;

  return 0;
}


