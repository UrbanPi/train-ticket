### Original description (from branch ts-error-process-seq-status(chance)-F12)
> Industrial fault description:
> 
> F12 is one kind of faults that occurs due to the specific status of some microservice.
> The word "status" has a wide range of meanings, for example, a global value in one microservice.
> If a microservice is in some specific "status", the fault occurs.
> This kind of faults only occurs in some specific status of a microservice.
> Because the fault only occurs in specific status, when we analyze the root cause of the microservice, we must combine the microservice status.
> 
> 
> TrainTicket replicated fault description:
> 
> We have two specific status in Order-Service: locked station and thread-pool size.
> If the admin is operating the orders between two stations, such two stations will be added to the locked station list.
> And the thread-pool is used for Order-Service to do some asynchronous tasks.
> If the user want to cancel a order whose start station or terminal station is in the locked station list, the request will be rejected.
> Then the fault occurs.


### Original fault replication (from branch ts-error-process-seq-status(chance)-F12)
> Setup System:
> 
> 1. Use docker-compose to setup the TrainTicket system.
> 2. Log in and make sure that there is at least one ticket order that fits the following:
>    (1) The train number is start with Z or K.
>    (2) The order status is PAID.
> 
> 
> Failure Triggering Usage Steps:
> 
> 1. Click [Admin Management] and login with admin account. (Username: adminroot ; Password: adminroot)
> 2. Enter "Shang Hai" and "Nan Jing" into the two input box at the upper right part of page.
> 3. Click [Search And Lock].
> 4. Return to the index page and login.
> 5. Click [Flow Two - Ticket Cancel & Ticket Change].
> 6. Click [All Orders Async].
> 7. Click [Refresh Orders].
> 8. Select the order mentioned above and click [Cancel Order].
> 9. You will get [Error] alert and see the exception logs on the server console.
> 
> 
> Failure Triggering Test Case:
> 
> There are two test cases in ts-ui-test, named [TestFlowFail.java] and [TestFlowSuccess.java] .
> Run [TestFlowFail.java] will reproduce the fault.
> Run [TestFlowSuccess.java] won't trigger the fault.


1. In the second step of the failure reproduction process enter "shanghai" and "nanjing" instead of "Shang Hai" and "Nan Jing"
   These are the internal IDs of these cities, which are used for checking if a station is locked.
2. There is a mismatch between the name of the branch and the name of the branch suggested by the descriptions in the repositories.
   The repositories suggest that **F12: ts-error-processes-seq-status(chance)-F12-Final** is the correct branch. Actually, the
   correct branch, which also represents the code contained in the zip package on https://fudanselab.github.io/research/MSFaultEmpiricalStudy/
   is **F12: ts-error-processes-seq-status(chance)-F12** (without 'Final').
3. There exists the possibility to trigger a second fault: when the stations, which are blocked (step 2 of original failure reproduction)
change during the short period when the cancelling of a ticket is processed, there is a mismatch between the blocked stations which triggers an error.
However, it seems unlikely that this fault can be triggered by manual execution of the workflows. 