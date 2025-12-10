
# Train Ticket：A Benchmark Microservice System
This is a fork of Trainticket from [FudanLab SE](https://github.com/FudanSELab/train-ticket), 
with revised error branches and instructions for setting up the system with the test case generator 
[EvoMaster](https://github.com/WebFuzzing/EvoMaster). 

For information on the system, adaptations and setup please visit the [Wiki](https://github.com/software-competence-center-hagenberg/train-ticket/wiki).
The individual branches do contain a rudimentary readme, acting as a short summary. Details are available in the wiki.

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



## Service Architecture Graph (from FudanLab SE)
![architecture](./image/2.png)





