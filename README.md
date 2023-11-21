### Original fault description:

> F13 is one kind of fault due to the wrong processing order of multiple requests.
> In a complex business process, we need send many requests in order to complete our business.
> However, if we send these requests in a short period of time(eg. fast click), these reqeusts may not be processed in order due to the transmission delay or some other reason.
> If the latter request needs the result of the previous request, such kind of fault like F13 will occur.
> 
> TrainTicket replicated fault description:
> 
> In TrainTicket system, if a user want to complete a ticket-booking process and a ticket-cancellation process, he/she will send many requests.
> These reqeusts includes login, searching for tickets, selecting contacts, confirming tickets, payment and comfirming cancellation.
> All these requests have a random delay to simulate the process delay.
> If the comfirming cancellation is already begun but the payment process is still not completed yet, this fault will occur.
> 
> 
> Fault Replicate:
> Visit http://10.141.212.21:12898/doErrorQueue/useAccount/sasdasdasdas@163.com/aaaaaaaa
> Sometimes it will success:
>     [Do Error Queue Complete No Exception]
> Sometime it will fail:
>     Whitelabel Error Page
>     This application has no explicit mapping for /error, so you are seeing this as a fallback.
>     Wed Jun 13 10:48:05 UTC 2018
>     There was an unexpected error (type=Internal Server Error, status=500).
>     [Error Queue]