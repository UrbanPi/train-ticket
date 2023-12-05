
### error-f3
#### Original fault description 

> ### Industrial fault description:
> 
> F3 is a fault which occurs when the microservice is not properly configured.
> If a micorservice is implemented by Java and using Docker as container, JVM and Docker configuration is needed.
> However, JVM and Docker both have same configuration such as memory limit and cpu limit, while configuration in JVM and configuration in Docker influences each other.
> If these configuration is not properly set, the microservice will have some unexpected behavior.
> 
> 
> 
> TrainTicket replicated fault description:
> 
> In the reproduction of F3, we mis-configured some microservice such that the JVM memory limit is bigger than the Docker memory limit.
> In this case, if the requests occupy too much memory, the JVM process will be killed, leading to the microservices unavailable periodly.
> Then the fault occurs.
> 
> ### Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Input "Shang Hai" in the start station and input "Su Zhou" in the end station.
> 2. Select date and click [Search]. Remeber to select high-speed train.
> 4. After a few seconds, it will alert [error].
> 
> Failure Triggering Test Case:
> 
> There are two test cases in ts-ui-test, named [TestFlowKill] and [TestFlowOOM].
> Just run [TestFlowKill] and it will do as failure triggering usage steps mentioned above.
> 
> Note:
> Every time you run it, order service crashes.
> Thus, you need to wait for the order service to restart if you want to run it one more time.
> Otherwise "Connection refused" will be printed in the terminal.

#### Notes

The failure happens as described after a few tries. The original description already states that the authors misconfigured
multiple services. The services are:

| Service                | Endpoint                     | Chance of failure |
|------------------------|------------------------------|-------------------|
| ts-train-service       | retrieve                     | 20%               |
| ts-basic-service       | queryForTravel               | 30%               |
| ts-order-service       | getTicketListByDateAndTripId | 100%              |
| ts-order-other-service | getTicketListByDateAndTripId | 100%              |



The misconfiguration of the services triggers with a certain randomness. Not every execution of the original fault
replication steps leads to a failure of `ts-order-service`, because `ts-order-service` depends on a successful call to
`ts-basic-service`. 