### error-f5
> ## Industrial fault description:
> 
> F5 is such kind of fault which is caused by the resource competition of multiple requests. Sometimes a microservice 
> has its maximum number of connections by using thread pool. Suppose we have 3 services, A, B, C. A and B both call C 
> for some specific information. If A send some requests to C, but before that B has sent some requests to C and these 
> requests are too complex to process at a short time, then the requests from A must wait until the requests from B 
> completed, leading to a timeout exception.
> 
> 
> ## TrainTicket replicated fault description:
> We implemented this fault in **Basic-Info-Service**. We use asynchronous tasks in Basic-Info-Service 
> to collect tickets information. Then we use the thread pool which is needed for the implementation of asynchronous tasks 
> as microservice resource. We send many requests at a short period of time and if the thread number is equal or exceeds the 
> max-thread-pool-size, the fault will occur.
> 
> ## Triggering the failure (via click-twice-service)
> 1. http://localhost:30078/click/occupy
> 2. Visit this address in another explorer tab quickly.
>    http://localhost:30078/click/auto
> 3. See the console, you will see some exception, fix it.


#### Notes
There is no `Basic-Info-Service`, however there are two other production services, which have a (too) small threadpool 
configuration:

| Service                 | Endpoint        | Core pool size | Max pool size | Blockingqueue capacity | Timeout                           |
|-------------------------|-----------------|----------------|---------------|------------------------|-----------------------------------|
| ticketinfo-service      | /queryForTravel | 2              | 3             | 10                     | 20s                               |
| inside-payment-service  | /pay /drawBack  | 1              | 1             | 1                      | 5s (for drawback), else unlimited |


The endpoint of ticketinfo-service should return some JSON, but it should also return null when called too fast, too often.
The endpoints of inside-payment-service return a boolean. The fault occurs when the service returns false, although it should have returned true.

To trigger the failure of `ticketinfo-service` it is sufficient to call `http://localhost:30078/click/occupy`. This 
triggers the following chain of calls five times: 

`ts-travel-plan-service` -> `ts-route-plan-service` -> `ts-travel2-service` -> `ts-ticketinfo-service` -> `ts-basic-service`

The last service `ts-basic-service` is important, because it introduces a delay of 10 seconds. Hence, the five requests,
which are sent by `click-twice-service` quasi at the same time, are enough to cause the failure, because the last of the
five requests has to wait at least for 20 seconds. In `ts-travel-plan-service`, `ts-route-plan-service` and `ts-travel2-service`
stacktraces from the exceptions show up in the logs.

Calling `http://localhost:30078/click/auto` triggers the same call chain from above once. Calling this endpoint in fast
succession also causes the failure from above.
