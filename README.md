### error-f7
#### Original fault description
> F7 is a fault which occurs in a third-party service and then leads to a failure.
> We always need to call a microservice that maintained by a third-party or company.
> Sometimes the response from the microservice maintained by others may be timeout and returns nothing, or even return wrong information.
> Then this kind of fault occurs.
> 
> ### TrainTicket replicated fault description:
> 
> In TrainTicket system, if the user want to buy a ticket but the balance is not enough, the system will call a third-party service implemented by Node.js to get the ticket money.
> Sometimes there will be a delay in this third-party service, then the timeout will be triggered and the fault occurs.
> 
> ### Fault Reproduce Steps #
> Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Select date and click [Search]. Remember to select [Others].
> 3. Select one Train-Number and click [Book].
> 4. Select one contacts and click [Select].
> 5. Click [Confirm Ticket] and wait for the [SUCCESS] alert.
> 6. Click pay for the ticket and wait for the result.
>    If no fault occurs, you will receive [SUCCESS].
>    If the fault occurs, you will receive [Pay Error] and see the exception logs in server console. 

#### Notes
The error can be seen in traces of `ts-inside-payment-service`

The description implies that there is a certain chance, that the third party service has a delay or not. However, this is not reflected by the implementation.
#### Actual implementation:
1. `ts-inside-payment-service` sends a request to the "external service" with: http://ts-rest-external-service:16100/greet and gives the request two seconds to complete.
2. In `ts-rest-external-service` the request is always handled after a delay of two seconds, therefore it is impossible that the request will be completed in the two-second timeframe specified by `ts-inside-payment-service`.
3. `ts-inside-payment-service` contains commented out code, which randomly selects either a two or six second timeout for 
the request to the external service. While this allows the request to finish successfully, this behaviour still does not
conform to the description, because `ts-rest-external-service` always has a delay of two seconds and not a random chance
for a delay. 

##### Other observations:
* `ts-inside-payment-service` contains a path during request handling where `ts-inside-payment-service` gets called again. However, this path can not be reached in this version of Train Ticket and the call also has no further effects on any of the two services.
* The original docker-compose.yml creates six replicas of `ts-rest-external-service`, which seem superfluous, because this service should not crash under normal circumstances.


##### Adapted implementation:
In order to respect the described chance for success or failure, I adapted the implementation of `ts-rest-external-service`:
* `ts-rest-external-service`: Added a random delay between 1.5 and 2.5 seconds.
* Did not adapt or activate code in `ts-inside-payment-service`, because these changes do not conform to the description.

##### Other changes:
* The kubernetes deployment only spawns one instance of `ts-rest-external-service`.

