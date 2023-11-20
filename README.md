Original description:
> This fault is caused by the error of redis in the operation of getting the saved key/token.
The microservice always save some key/token to redis.
However, sometimes the developer may made a mistake and the program may be mis-implemented.
In such case, the key/token may be wrongly read and deliver a missing/wrong key/token to other microservice, leading to an fault.
>
>
>
> TrainTicket replicated fault description:
>
> We have two types of users in TrainTicket system: normal user and VIP user.
> Compared to the normal user, the VIP user has one more key/token to be used in ticket-booking process.
> However, when vip user is processing ticket-reservation logic, the key/token is missing when delivering.
> Then the fault occurs.


Original replication steps:

>Setup System:

>1. Use docker-compose to setup the TrainTicket system.
>2. Log in and make sure that there is at least one ticket order that fits the following:
    >   (1) The train number is start with Z or K.
    >   (2) The order status is PAID.
>
>
>Failure Triggering Usage Steps:
>
>1. Log in with the vip username "vip_microservices@163.com" and password "DefaultPassword".
>2. Click [Flow Two - Ticket Cancel & Ticket Change].
>3. Click [Refresh Orders].
>4. Select the order mentioned above and click [Cancel Order].
>5. Click [Confirm Cancel].
>6. You will get error alert and see the exception logs on the server console.
>
>Failure Triggering Test Case:
>
>There are two test cases in ts-ui-test, named [TestFlowFail.java] and [TestFlowSuccess.java].
>Run [TestFlowFail.java] will reproduce the fault.
>Run [TestFlowSuccess.java] won't trigger the fault.


1. There is no user with username "vip_microservices@163.com" and password "DefaultPassword". There are just the normal logins for a normal user and the admin user.
2. At least with the normal booking workflow it is impossible to create the scenario as described by the setup step two, because selecting any train connection for further booking fails.
3. This fail is due to the implementation. In this step of the use case, the contacts-service should send the login token from the user to the sso-service for verification.
   However, the contacts-service always sends a string "null" to the sso-service, which then fails to verify this token.

Based on the implementation the fault in this branch revolves around failing calls to any of these endpoints from contacts-service:
* /contacts/findContacts
* /contacts/delete

One way of triggering this fault is to try to book a ticket for any train. Trying to select any train connection for further booking steps will fail.