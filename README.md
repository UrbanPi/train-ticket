## ts-error-F15
### Original fault description
> **industrial fault description**:
> 
> Symptom：
> 
> The data-synchronization job quits unexpectedly
> 
> Root Cause：
> 
> The spark actor is used for the configuration of actorSystem (part of Apache Spark) instead of the system actor
> 
> **train_ticket replicated fault description**:
> 
> Limit the post json size to 200 bytes in nginx.conf file.
> If user select the food and consign, the request body will exceed 200 bytes, and the request will be blocked by nginx
> 
> **fault replicate steps**:
> 
> setup system:
> 
> - Use docker-compose to setup the Train-Ticket System.
> 
> fault reproduce manually step:
> 
> 1. Select [Flow One - Ticket Reserve]
> 2. Log in and select a data, Click [Search]
> 3. Select one searching results, click the [Booking] button 
> 4. Select a contacts, check [Need Food], select [Station Food Stores] and select one food as you like
> 5. Check [Consign] and input the corresponding information, click [Select] 
> 6. Click the [Confirm Ticket] in step4
> 5. You will get the alert which says "Preserve Failed"
> 
> If you want to reserve ticket successfully, uncheck the [Need Food] and [Consign]

### Notes

Works as described :) 
Clarification: selecting either food or consigning exceeds the request limit. Selecting a traffic assurance does not 
exceed the limit.