## error-f19

###  Original fault description
>
> Industrial fault description:
> 
> The price is displayed in an unexpectedly format.
> The product price is not formatted correctly in the French format.
> 
> 
> TrainTicket replicated fault description:
> 
> When the user chooses to consign his packages and select the French format, the returned price is displayed in wrong format.
> The product price is not formatted correctly in the French format.
>
>
> Symptom:
> When the user chooses to consign his packages and select the French format, the returned
> price is displayed in wrong format
> 
> ###Root Cause:
> The product price is not formatted correctly in the French format
    
### Notes 
Works as described. This error only appears when consigning, and it only changes the formatting i.e. changing 
spaces, commas, points as delimiters and choosing a currency symbol. Hence, the monetary value stays the same no matter
the currency. 