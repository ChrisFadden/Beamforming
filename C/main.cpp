#include<stdio.h>
#include "hdf5.h"

int main(int arg, char** argv){
	
	hid_t file_id, dataset_id, dataspace_id;
	hsize_t dims[2];
	herr_t status;
	
	//Create file
	file_id = H5Fcreate("test.h5",H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
	
	//Create Data Space
	dims[0] = 4;
	dims[1] = 6;
	dataspace_id = H5Screate_simple(2,dims,NULL);

	//Create Data Set
	dataset_id = H5Dcreate2(file_id,"/dset",H5T_STD_I32BE, dataspace_id,
													H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);

	//Close Data Set
	status = H5Dclose(dataset_id);

	//Close Data Space
	status = H5Sclose(dataspace_id);	

	//Close File
	status = H5Fclose(file_id);

	printf("Hello World\n");

	return 0;
}
