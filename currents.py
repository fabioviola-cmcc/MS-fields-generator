#!/usr/bin/python3

# global requirements
import os
import pdb
import sys
import numpy
import warnings
import traceback
from netCDF4 import Dataset

# disable warnings
warnings.filterwarnings("ignore")

# main
if __name__ == "__main__":

    # read input filename
    inputFilenameU = sys.argv[1]
    inputFilenameV = sys.argv[2]

    # read and set variables
    latVar, lonVar, timeVar = sys.argv[3].split(":")
    uVar = "vozocrtx"
    vVar = "vomecrty"
        
    # open a netcdf file for currents
    inputFileU = Dataset(inputFilenameU)
    inputFileV = Dataset(inputFilenameV)
    
    # determine date from input filename
    refdate = os.path.basename(inputFilenameU)[15:21]

    # set the output directory
    outputDir = sys.argv[4]
    

    #####################################
    #
    # --- for output file 1 ---
    #
    #####################################

    # iterate over timesteps
    for t in range(len(inputFileU.variables[timeVar])):

        # create file
        outputFilename1 = os.path.join(outputDir, "curr_vector_%s_%02.d.nc" % (refdate, t))
        outputFile1 = Dataset(outputFilename1, "w", format="NETCDF4")
        print(" == Generating %s" % outputFilename1)
        
        # --- create dimensions ---
        outputFile1.createDimension("lat", len(inputFileU.variables[latVar]))
        outputFile1.createDimension("lon", len(inputFileU.variables[lonVar]))
        outputFile1.createDimension("components", 2)
        outputFile1.createDimension("string1", 1)
        
        # --- create variables ---
        comp = outputFile1.createVariable("components", "S1", ("components", "string1"))
        lat = outputFile1.createVariable("lat", "f4", ("lat", ))
        lon = outputFile1.createVariable("lon", "f4", ("lon", ))
        u = outputFile1.createVariable("u", "f4", ("lat", "lon", ))
        v = outputFile1.createVariable("v", "f4", ("lat", "lon", ))
        curr = outputFile1.createVariable("curr", "f4", ("components", "lat", "lon", ), fill_value=-999)
        
        # --- fill variables ---
        comp[:] = ["u", "v"]                    
        lat[:] = inputFileU.variables[latVar][:]
        lon[:] = inputFileU.variables[lonVar][:]
        curr[0,:,:] = inputFileU.variables[uVar][t,0,:,:]
        curr[1,:,:] = inputFileV.variables[vVar][t,0,:,:]
        u[:,:] = inputFileU.variables[uVar][t,0,:,:]
        v[:,:] = inputFileV.variables[vVar][t,0,:,:]
        
        # close output file
        outputFile1.close()

    
    #####################################
    #
    # --- for output file 2 ---
    #
    #####################################

    # iterate over timesteps
    for t in range(len(inputFileU.variables[timeVar])):

        # create file
        outputFilename2 = os.path.join(outputDir, "curr_intensity_%s_%02.d.nc" % (refdate, t))
        outputFile2 = Dataset(outputFilename2, "w", format="NETCDF4")
        print(" == Generating %s" % outputFilename2)
        
        # --- create dimensions ---
        outputFile2.createDimension("lat", len(inputFileU.variables[latVar]))
        outputFile2.createDimension("lon", len(inputFileU.variables[lonVar]))
        
        # --- create variables ---
        lat = outputFile2.createVariable("lat", "f8", ("lat", ))
        lon = outputFile2.createVariable("lon", "f8", ("lon", ))
        curr = outputFile2.createVariable("curr", "f8", ("lat", "lon", ), fill_value=-999)

        # --- fill variables ---
        lat[:] = inputFileU.variables[latVar][:]
        lon[:] = inputFileU.variables[lonVar][:]
        curr[:] = numpy.sqrt(numpy.square(inputFileU.variables[uVar][t,0,:,:]) + numpy.square(inputFileV.variables[vVar][t,0,:,:]))
        
        # close output file
        outputFile2.close()
