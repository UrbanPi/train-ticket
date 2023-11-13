

## Industrial fault description:

F7 is a fault which occurs in a third-party service and then leads to a failure.
We always need to call a microservice that maintained by a third-party or company.
Sometimes the response from the microservice maintained by others may be timeout and returns nothing, or even return wrong information.
Then this kind of fault occurs.



## TrainTicket replicated fault description:

In TrainTicket system, if the user want to buy a ticket but the balance is not enough, the system will call a third-party service implemented by Node.js to get the ticket money.
Sometimes there will be a delay in this third-party service, then the timeout will be triggered and the fault occurs.





## Fault Reproduce ##


# Fault Reproduce Steps #
Failure Triggering Usage Steps:

1. Log in.
2. Select date and click [Search]. Remember to select [Others].
3. Select one Train-Number and click [Book].
4. Select one contacts and click [Select].
5. Click [Confirm Ticket] and wait for the [SUCCESS] alert.
6. Click pay for the ticket and wait for the result.
   If no fault occurs, you will receive [SUCCESS].
   If the fault occurs, you will receive [Pay Error] and see the exception logs in server console.
