### ts-error-F17

> **industrial fault description**:
> 
> Symptom：
> The grid-loading process takes too much time
> 
> Root Cause：
> Too many nested “select” and “from” clauses are in the constructed SQL statement
> 
> **train_ticket replicated fault description**:
> 
> To simulate the nested select clauses, one procedure of mysql to sleep 10s was created in ts-voucher-service.
> Since the front stage has a 5s limit of network request, the query of one order's voucher will be out of time.
> 
> **fault replicate steps**:
> 
> setup system:
> 
> - Use docker-compose to setup the Train-Ticket System.
> 
> fault reproduce manually step:
> 
> 1. Click [Flow One - Ticket Reserve] and Log in
> 2. Click [Flow Three - Consign & Voucher]  and click [Refresh Orders] of [Step1:- View My Orders] 
> 3. Select one order and click its [Print Voucher] button
> 4. You will get the "Timeout" alert 


### Notes
Works as described. After step four, none of the links on the website work anymore. To get back one has to use the back
button of the browser. (Tried out on Firefox and Edge)