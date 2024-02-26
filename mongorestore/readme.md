# Init container "mongorestore"
This init container contains the binary **mongorestore** from the package `mongodb-database-tools-debian11-x86_64-100.9.4`. 
We need this binary to restore the initial states of the MongoDBs in the error branches when generating tests with EvoMaster.
We could have included this binary in the "persinit" (PersistenceInit) containers of the error branches but refuse to,
to keep the container sizes small.