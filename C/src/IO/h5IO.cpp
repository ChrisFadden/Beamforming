#include "h5IO.h"
#include "hdf5.h"
void h5IO::inputMat(const char* fn, const char* group, arma::Mat<double> &B){
	
	/********************
	 * Initialize Types
	 *******************/	
	hid_t file_id, dataset_id;
	hid_t dataspace, datatype;
	int status_n;	
	hsize_t	dims[2] = {0, 0};
	herr_t status;	
	
	/********************
	 * Set Matrix to HDF5
	 *******************/
	file_id = H5Fopen(fn,H5F_ACC_RDONLY,H5P_DEFAULT);
	dataset_id = H5Dopen2(file_id, group,H5P_DEFAULT);

  dataspace = H5Dget_space(dataset_id);    /* dataspace handle */
  status_n  = H5Sget_simple_extent_dims(dataspace, dims, NULL);
	
	datatype = H5Dget_type(dataset_id); 
	
	double* dataArray = (double*) malloc(dims[0]*dims[1]*sizeof(double));

	status = H5Dread(dataset_id, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL,
				 H5P_DEFAULT, dataArray);
	
	arma::Mat<double> A(dataArray,dims[1],dims[0]);	
	B = A;

	/**********************
	 * Delete Pointers
	 *********************/	
	free(dataArray);	
	status = H5Sclose(dataspace);
	status = H5Dclose(dataset_id);
  status = H5Fclose(file_id);
	
	return;
}
