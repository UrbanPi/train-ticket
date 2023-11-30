## ts-error-F22

### Original fault description from readme
> ### Symptom：
> When the user switch to Flow Three - Consign & Voucher
> and click the button of "Print Voucher" if any,
> the result page displays "Empty. No data!".
> 
> ### Root Cause
> The constructed SQL statement includes a wrong column name
> in the “select” part according to its “from” part

### Original fault description from "Document" directory
(Struck through wrong information)

> Industrial fault description:
> 
> The error of SQL column missing is returned upon some data request.
> The constructed SQL statement includes a wrong column name in the "select" part according to its "from" part
> 
> 
> TrainTicket replicated fault description:
> 
> The constructed SQL statement includes a wrong column name in the "select" part according to its "from" part.
> When the user switch to Flow Three - Consign & Voucher and click the button of "Print Voucher" if any, the result page displays "Empty. No data!".
> 
> ~~Failure Triggering Usage Steps:~~
> 
> ~~1. Log in.~~
> ~~2. Click [Flow Two - Ticket Cancel & Ticket Change].~~
> ~~3. Click [Refresh Orders].~~
> ~~4. Select the order mentioned above and click [Cancel Order].~~
> ~~5. Click [Confirm Cancel].~~
> ~~6. You will get result of cancel. If you get SUCCESS, it means the fault does not occur.~~
>    ~~If you get WRONG, it means the fault occurs, and you will see the exception logs on the server console.~~
> 
> 
> ~~Failure Triggering Test Case:~~
> 
> ~~There is only one test case in ts-ui-test, named [TestFlowTwoCancel.java].~~
> ~~Just run it and it will do as failure triggering usage steps mentioned above.~~

### Notes
**Clarification**: In the context of this system the term *voucher* has the meaning *receipt* or *invoice* and not *coupon* or *gift card*.

The original description in conjunction with specific interpretation of the term *voucher*, can lead to inability to 
reproduce the failure. In the previous branches the descriptions contained in the "Document" directory were mostly correct
but this time the steps to trigger the failure are wrong. The contents of the original readme on the other hand are incomplete,
because they lack information on the necessary preconditions which have to be fulfilled in order for the "Print Voucher" 
button to appear. The correct steps are:

1. Log in.
2. Complete **all** steps in **Flow One - Ticket Reserve**. (Note: tripIds starting with **T** or **Z** are **not** able to finish all steps). Example journey: Shang Hai -> Su Zhou
3. Click [Flow Two - Ticket Cancel & Ticket Change].
4. Click [Refresh Orders].
5. Click **Print voucher** on the previously bought and used ticket.
6. The table on the next page should display 'Empty. No data!' instead of the actual ticket data.
7. (To get to the previous page, you have to use the 'Back' button of your browser.)


