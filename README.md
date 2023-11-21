Reproduce Procedure:
1.Login
2.View Orders.
3.Cancel Tickets (Normal Ticket)
Sometimes it will success.
Sometimes it will throws exception.
You should figure out why sometimes fail, sometimes success .
Then you should debug to make sure success all the time.


### Original description

> F11 is a fault due to the lack of sequence control.
> Note that such a fault may not always occur, making  it difficult to analyze.
> Sometimes if a return value is too far from the normal value, the microsevice will recheck the correctness of the value and correct it.
> But this process does not always happen, making the result sometimes wrong but sometimes right.
> 
> 
> 
> TrainTicket replicated fault description:
> 
> In TrainTicket system, there are two microservices set the same value in the database in order cancellation process.
> Due to the lack of control like F1, the two microservices may set the value in a wrong sequence.
> However, the second microservice that set the value may recheck the value and correct the value.
> The recheck process does not always happen.
> If two microservices set the value in a wrong sequence but the recheck process does not executed, this fault occurs.
> 
> 
> Setup System:
> 
> 1. Use docker-compose to setup the TrainTicket system.
> 2. Log in and make sure that there is at least one ticket order that fits the following:
>    (1) The train number is start with Z or K
>    (2) The order status is PAID
> 
> 
> Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Click [Flow Two - Ticket Cancel & Ticket Change].
> 3. Click [Refresh Orders].
> 4. Select the order mentioned above and click [Cancel Order].
> 5. Click [Confirm Cancel].
> 6. You will get result of cancel. If you get [SUCCESS] means the fault do not occur.
>    If you get [Error] alert, that means the fault occurs, and you will see the exception logs on the server console.
> 
> 
> Failure Triggering Test Case:
> 
> There is only one test case in ts-ui-test, named [TestFlowOne.java].
> Just run it and it will do like failure triggering usage steps mentioned above.
> 






