### error-f4

#### Original fault description
> Industrial fault description:
> 
> F4 is fault of SSL offloading which leads to the response time for some requests is very long.
> 
> 
> TrainTicket replicated fault description:
> 
> In TrainTicket system, we apply SSL to every microservice.
> When we send requests about some complex logic, we will find that the response time is very long.
> In this scenario, the faults occurs.
> 
> Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Click [Flow One - Ticket Reserve].
> 3. Select date and click [Search].
> 4. Select one Train-Number and click [Book].
> 5. Select one contacts and click [Select].
> 6. Click [Confirm Ticket].
> 7. Click [Pay].
> 8. If the result returns after an acceptable time period, it is succeeded.
>    But if the response time is very long, then it fails and the fault occurs.
> 
> 
> Failure Triggering Test Case:
> 
> There is only one test case in ts-ui-test, named [TestFlowOne.java].
> Just run it and it will do as failure triggering usage steps mentioned above.
> 

#### Notes
At least on the local deployment (WSL, docker desktop, minikube, 14 cores, 64GB RAM) the whole system or at least the 
ticket booking process does not seem really fast. Hence, without measuring the time between individual actions and comparing
them to the same actions in the non-ssl version, the described failure can not be confirmed just by following the steps
above. 

The implementation does use ssl in every service.