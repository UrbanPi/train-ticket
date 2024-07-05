Adapted implementation of EvoMaster to make it work with the login of TrainTicket. 
Changes are marked with a comment starting with `Pirmin Urbanke:`
Both files are from EvoMaster/core, the detailed location can be 
inferred from the package definition (first line in the files).

We used EvoMaster 2.0.0. You should be able to simply replace the files and compile 
EvoMaster, complying to instruction in the EvoMaster repository, to obtain the adapted executable.
Since the adaptions do not alter the communication between the EvoMaster main executable and the 
white-box driver the white-box driver available from Maven can be used without fear.
