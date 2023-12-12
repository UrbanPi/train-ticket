### error-f9

#### Original fault description
> There is a Right To Left (RTL) display error for UI words.
> There is a CSS display style error in bi-directional.
> 
> 
> TrainTicket replicated fault description:
> 
> Fault occurs when convert from LTR to RTL in Login Block.
> 
> Setup System:
> 
> 1. Use docker-compose to setup the TrainTicket system.
> 
> 
> Failure Triggering Usage Steps:
> 
> Click the [RTL] button at the top of the page and you will see the typographical fault.

#### Notes
It is hard to tell where the actual fault is, because on the entire page there are multiple places which could be 
considered as faulty e.g. on the page `Flow One - Ticket Reserve`:
1. Login indicator: one time it shows as `== Login User ID4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f` (probably the described 
fault). The other time it shows as `Login User ID == 4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f`
2. On the entire page the section headings switch from flushed left to flushed right when pressing the button 
`Convert To RTL/LTR`.
3. In `Ticket Reserve Step 3 - Select Contacts`: The label of the `Need Food` checkbox is partially hidden by the checkbox.

This fault sticks out to the other faults, because this fault is a pure (CSS) style issue which has no connection to the
backend services. 