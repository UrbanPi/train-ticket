# F5: ts-error-cross-timeout-status(chance)-F5
## Industrial fault description:

F5 is such kind of fault which is caused by the resource competition of multiple requests. Sometimes a microservice 
has its maximum number of connections by using thread pool. Suppose we have 3 services, A, B, C. A and B both call C 
for some specific information. If A send some requests to C, but before that B has sent some requests to C and these 
requests are too complex to process at a short time, then the requests from A must wait until the requests from B 
completed, leading to a timeout exception.


## TrainTicket replicated fault description:
We implemented this fault in **Basic-Info-Service** (Comment: There is no Basic-Info-Service, however, there are two 
other production services, which have a small threadpool configuration). We use asynchronous tasks in Basic-Info-Service 
to collect tickets information. Then we use the thread pool which is needed for the implementation of asynchronous tasks 
as microservice resource. We send many requests at a short period of time and if the thread number is equal or exceeds the 
max-thread-pool-size, the fault will occur.

### ExecutorConfig of ticketinfo-service: 
````    
    /** Set the ThreadPoolExecutor's core pool size. */  
    private int corePoolSize = 2;
    /** Set the ThreadPoolExecutor's maximum pool size. */ 
    private int maxPoolSize = 3;
    /** Set the capacity for the ThreadPoolExecutor's BlockingQueue. */  
    private int queueCapacity = 10;
````
Call
````
/ticketinfo/queryForTravel
````
This endpoint should return some JSON, but it should also return null when called too fast, too often.


### Executor Config of inside-payment-service:
````    
    private int corePoolSize = 1;
    private int maxPoolSize = 1;
    private int queueCapacity = 1;
````
Call 
````
/inside_payment/pay
/inside_payment/drawBack
````
These endpoints return a boolean. The fault occurs when the service returns false, although it should have returned true.