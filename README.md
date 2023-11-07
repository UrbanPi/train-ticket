
# Description (copied original description)
## Industrial fault description:

F1 is a fault that occurs in using asynchronous tasks in a single request, when we send messages asynchronously without message sequence control.
Suppose we have Event A and Event B in a request, while Event A always processes and returns earlier than Event B.
But sometimes, due to some specific reasons, Event A processes and returns later than Event B.
Then F1 will occur.



## TrainTicket replicated fault description:

In ticket-cancellation logic of the TrainTicket system, we have two major events: [Drawback Money] and [Reset Order Status].
If the user decided to cancel an order, the Ticket-Cancel-Service firstly call Inside-Payment-Service to drawback money.
Then Inside-Payment-Service call Order-Service to set the order status to CANCELLING.
Then the system refunds the money to user.
After that, the Cancel-Service call Order-Service set the order status to CANCEL.
Then the whole cancel process is done.
In our fault reproduction, we made a random delay in event [Drawback Money] to simulate the situation of network congestion.
In this case, the event [Reset Order Stauts] will complete before [Drawback Money], then the fault occurs.



## Fault replication

Failure Triggering Usage Steps:

1. Log in.
2. Click [Flow Two - Ticket Cancel & Ticket Change].
3. Click [Refresh Orders].
4. Select the order mentioned above and click [Cancel Order].
5. Click [Confirm Cancel].
6. You will get result of cancel. If you get SUCCESS, it means the fault does not occur.
   If you get WRONG, it means the fault occurs, and you will see the exception logs on the server console.


Failure Triggering Test Case:

There is only one test case in ts-ui-test, named [TestFlowTwoCancel.java].
Just run it and it will do as failure triggering usage steps mentioned above.
