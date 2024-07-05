# TrainTicket execute / util branch
This branch contains various helper scripts for working with and executing TrainTicket.
If you plan to work with this repository you should consider copying following directories
outside the TrainTicket repository:
* execute_evo_master
* execute_evo_master_tests
* update_files_in_branches
* util


# Overview

The repository contains various versions of the Trainticket microservice system.
The master and ts-error-cleaned branch have no deliberately built-in faults, the remaining branches each
contain a deliberately built-in fault. The master branch and the fault branches
also differ from each other with regard to the underlying tech stack. Most notably:

| Component          | master branch      | fault branches                |
|--------------------|--------------------|-------------------------------|
| Primary framework  | SpringBoot 2.3.12  | SpringBoot 1.5.3              |
| Persistence:       | One MySQL*         | Mostly individual MongoDBs    |
| Service discovery: | Spring Cloud Nacos | No                            |
| End user GUI:      | Yes                | No (just for testing purpose) |
| Admin GUI:         | Yes                | Yes                           |


&ast;The MySQL persistence can be configured s.t. each service has its individual database server. In the experiments we
used one database instance/server for all services.

Kubernetes is used to run the system. We heavily rely on 'InitContainers' to
set up tracing, monitoring and running EvoMaster. Therefore, we need additional
containers besides the containers with the 'production' services. Most of these helper
containers are the same across all branches, hence we only include the files to build
these containers in the master branch. We include branch-specific helper containers in
the respective branches.

## Quickstart Trainticket with EvoMaster
1. Have Docker and Kubernetes setup -> see Wiki of this repository
2. Download / clone your preferred version of Trainticket into a ( WSL2) Linux distribution
3. Pull the following containers to ensure they exist (Background: There was/exists a problem with the private Github 
   container registry that prevents the download of external container dependencies)
```   
docker pull openresty/openresty:trusty
docker pull openjdk:8-jdk
docker pull python:3
docker pull node
docker pull mrrm/web.go
docker pull alpine:3.14
docker pull openjdk:8-jre
   ```
4. cd into root folder of the repo and start Trainticket with
   ``
   ./hack/deploy/deploy.sh default "--with-otel --with-monitoring"
   ``

5. Wait around 3 minutes. You can check the status with ``kubectl get pods``.
6. Start the production Java services with the Python script ``start_all.py``. Or start generating tests with EvoMaster
   by executing the Python script ``run_evo_master_test_generator.py``.
7. Wait again for around 3 minutes.
8. You can reach the endpoints of the individual services on different ports on localhost. The mappings of ports to services
   are hardcoded. They are defined in the Python script ``service_availability.py``.
9. stop Trainticket with
   ``
   ./hack/deploy/specific-reset.sh default "--with-otel --with-monitoring"
   ``

### Endpoints
* http://localhost:32677/  : GUI of Trainticket
* http://localhost:32677/adminlogin.html  : Admin GUI of Trainticket
* http://localhost:30003/  : Prometheus
* http://localhost:32688/  : Jaeger
* http://localhost:300XX/swagger-ui.html : Swagger definition of the production service (takes some time to load)
* http://localhost:303XX/swagger-ui.html : Prometheus endpoint of the production service (fast)
* http://localhost:306XX/swagger-ui.html : Swagger definition of the microservice controller

# Cloning, compiling, building, publishing
Use the contents of the python script in util/clone_branches.py to generate output for cloning, compiling the project and
building and publishing docker images.

## Compile Maven projects
You need to have Maven available. Go to the root folder and execute:

``mvn -DskipTests=true clean package``

## Build Docker containers
Prerequisite: Compiled Maven projects
`./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket branch_name`

### Production containers

Prerequisite: Compiled Maven projects

``./script/publish-docker-images.sh containers.github.scch.at/contest/trainticket <BRANCH_NAME>``

### Helper containers

#### EvoMaster

Includes a slightly customised version of EvoMaster (release 2.0.0) and the unmodified EvoMaster Java Client (release
2.0.0).

#### JavaxServlet

Includes the javax.servlet-api4.0.1.jar required for our custom OTEL agent.

#### mongorestore

Includes the 'mongorestore' binary from the package 'mongodb-database-tools-debian11-x86_64-100.9.4'.
Required to restore the initial state of the mongoDBs during test generation with EvoMaster.

#### OTEL

##### otel_agent

Our customised OTEL agent for instrumenting the production services.

##### otel_collector

A simple Java program acting as a target for the traces collected by the otel agents.

#### microservicecontroller

A wrapper program, which can start and stop a production service with and without EvoMaster client and which also starts
EvoMaster to generate tests.

#### PersistenceInit

Includes dumps from the persistence to enable resetting to the initial state. Specific for each branch.


