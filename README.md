## Original fault description:

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

##  Notes on original implementation
The `launcher-service` provided by the authors offers a simple way to execute a workflow of `login -> ticket_booking -> payment -> cancellation`. 
The delays in the respective services are:
*  500ms for logging in via `ts-login-service` in AccountLoginServiceImpl
* 5000ms for paying for a ticket via `ts-inside-payment-service` in InsidePaymentController
*  500ms for canceling the ticket via `ts-cancel-service` in CancelServiceImpl

Although these are random wrt. that there is no specific reason why the delay in `ts-inside-payment-service` has to be 
5000ms these are constant values even if `Thread.sleep(long)` gives no guarantees on the actual sleep time. Hence, the
provided description can be seen as misleading, because it suggests that there are random delays and that a call to
`launcher-service` sometimes fails and sometimes succeeds. Actually, sending single requests via `launcher-service`
allways fails, because cancellation of the ticket is allways finished before the payment is completed. Another
way to theoretically trigger a fault is to send multiple requests to `launcher-service` with the same account, which invalidates one
of the sessions, which prevents booking, paying and cancelling tickets. However, in the original implementation of `launcher-service`
this is not reported as an error.

The `launcher-service` reserves a ticket for a train with a `tripId` starting with `Z`, which should also be possible through
the user interface. However, this is not possible due to a change `ts-preserve-other-service PreserveOtherServiceImpl#preserve()`,
which was likely made to make `launcher-service` work as expected. Originally the service allways generated a random orderId
but after the change it expects the orderId to be sent with the request. Since the user interface does not send the orderId
in the payload the request fails.


## Adaptations

* In `ts-launcher AsyncTask#sendOrderTicket()`: Adapted the date of the journey to allways be one day in the future. Originally
a fixed timestamp was used, which lies in the past now.
* In `ts-launcher LauncherServiceImpl#doErrorQueue()`: Changed return type to `String` to return details on the current error.
* In `ts-launcher LauncherServiceImpl#doErrorQueue()`: Treat invalid user sessions due to multiple logins of the same user as an error.
* In `ts-inside-payment-service InsidePaymentController#pay()`: Add 50:50 chance for any invocation of this method to have a delay of 5000ms.
* In `ts-preserve-other-service PreserveOtherServiceImpl#preserve()`: Generate a random orderId as fallback when no orderId is provided in the request.
