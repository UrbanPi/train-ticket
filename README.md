### error-f8
#### Original fault description:
> This fault is caused by the error of redis in the operation of getting the saved key/token.
The microservice always save some key/token to redis.
However, sometimes the developer may made a mistake and the program may be mis-implemented.
In such case, the key/token may be wrongly read and deliver a missing/wrong key/token to other microservice, leading to an fault.
>
> TrainTicket replicated fault description:
>
> We have two types of users in TrainTicket system: normal user and VIP user.
> Compared to the normal user, the VIP user has one more key/token to be used in ticket-booking process.
> However, when vip user is processing ticket-reservation logic, the key/token is missing when delivering.
> Then the fault occurs.
> 
> 
> Setup System:

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

#### Notes

##### First attempt, source 'ts-error-redis-F8'
This is the first attempt of setting up this branch. 'ts-error-redis-F8' is the branch mentioned in the fault replication
GitHub repository. Based on the change history provided by git commits over different branches concerning *error-F8* 
we identified `ts-cancel-service`, `ts-sso-service` and `ts-contacts-service` as the services relevant in for this error.
By comparing SHA256 hashes of the source code of these services, we are sure that the code of this error branch and the
code provided as a zip archive at https://fudanselab.github.io/research/MSFaultEmpiricalStudy/ are the same.

1. There is no user with username "vip_microservices@163.com" and password "DefaultPassword". There are just the normal 
logins for a normal user and the admin user. The class initializing this data is `initData`, located in the sources of 
`ts-sso-service`.
2. At least with the normal booking workflow it is impossible to create the scenario as described by the setup step two, 
because selecting any train connection for further booking fails.
3. This fail is due to the implementation. In this step of the use case, the contacts-service should send the login token 
from the user to the sso-service for verification. However, the contacts-service always sends a string "null" to the 
sso-service, which then fails to verify this token.

Based on the implementation the fault in this branch revolves around failing calls to any of these endpoints from contacts-service:
* /contacts/findContacts
* /contacts/delete

One way of triggering this fault is to try to book a ticket for any train. Trying to select any train connection for further booking steps will fail.

##### Second attempt, source 'ts-error-redis-F8-basic'
In the second attempt we use the branch 'ts-error-redis-F8-basic', because it is one version which contains a VIP user
in its initial setup and judging by its name it should be the most basic version. 

1. Login works as described, and orders are present.
2. To activate the builtin fault one has to revert a change made in a git commit. (See original code snippet below)
3. When trying to cancel **any** ticket with the VIP user on the website, there is no info indicating that the request
failed and also the response code (code 200) or response body does not indicate any failure. In the backend however an
exception leading to a stacktrace in `ts-cancel-service` thrown.
4. As stated in the previous point the failure happens not only with trains starting with 'Z' or 'K' but also with other 
trains e.g. 'D'. 
5. The description states that the VIP user has or needs to provide one additional token in order to proceed in the ticket
booking process. This is wrong, because the relevant part of the original implementation in
`ts-cancel-service:CancelController#cancelTicket()` looks like this:
`````java
Account account = result.getAccount();
if(account.getName().contains("VIP")){
    return cancelService.cancelOrder(info, loginToken, loginId);
}else{
    return cancelService.cancelOrder(info, loginToken, loginId);
}
`````
To activate the fault the `loginToken` in the true-branch has to be replaced with something else e.g. `loginId`. We
know this, because there is a git commit which fixes the implemented fault with this change. With this knowledge it is 
also clear, why the failure happens with other trains than 'Z' or 'K'. The implemented fault does not distinguish between
the train types.

#### Adaptations
In xxxxx changed snippet:
`````java
Account account = result.getAccount();
if(account.getName().contains("VIP")){
    return cancelService.cancelOrder(info, loginToken, loginId);
}else{
    return cancelService.cancelOrder(info, loginToken, loginId);
}
`````
To: 
`````java
Account account = result.getAccount();
if(account.getName().contains("VIP")){
    return cancelService.cancelOrder(info, "Deliberately missing token", loginId);
}else{
    return cancelService.cancelOrder(info, loginToken, loginId);
}
`````