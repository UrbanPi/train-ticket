## ts-error-F20

### Original fault description

> Industrial fault description:
> 
> Nothing is returned upon workflow data request.
> The JBoss startup classpath parameter does not include the right DB2 jar package.
> 
> 
> TrainTicket replicated fault description:
> 
> Many microservices share a same lib. This lib contains some basic data structure such as Enum of Order status.
> The value of same order status in different version is in different value.
> If some microservice use an old version lib but some use a new version lib, the fault will occur.

> Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Click [Flow Two - Ticket Cancel & Ticket Change].
> 3. Click [Refresh Orders].
> 4. Click [Cancel Order].
> 5. The number of money is [Error].



### Notes:

Works as mostly as described. The order which will be cancelled has to be paid first in order for the failure to show. 