### error-f10

#### Original description (ts-error-logic-F10)
> F10 is simply a normal logic fault in one business process.
> This kind of fault occurs due to the defects in the implementation of a business process.
>
>
>
> train_ticket replicated fault description:
>
> In our Train Ticket System, the name and the ID Card number is required for booking a ticket.
> In our society, one ID card number only mapping one name.
> Thus, if two user input two distinct name but the document number is same, one of the user must be rejected.
> In our system, if one  document number has been occupied by one name, another user inputs the same document number but
> another name, he/she still successfully gets a ticket.
> In this scenario, a logic fault like F10 occurs.
>
>
> Fault reproduction:
> 1. Log in
> 2. Select date and click [Search]. Remeber to select [Others]
> 3. Select one Train-Number and click [Book].
> 4. At the first time you refresh contacts list, the list is empty.
     >    Input a new contact info and click [Select]
> 5. Click [Confirm Ticket] and wait for the SUCCESS alert.
> 6. At the second time you refresh contacts list, the list has one contact.
     >    Input a new contact info with the same document number with the first time and click [Select]
> 7. Click [Confirm Ticket] and wait for the ERROR alert.
> 8. At the third time you refresh contacts list, the list has two contact.
     >    Input a new contact info with the same document number with the first time and click [Select]
> 9. Click [Confirm Ticket] and wait for the ERROR alert.


#### Original description (ts-error-normal-F10)
>Reproduce Process:
>    1. Login
>    2. Search for "Nan Jing" and "Other"
>    3. Add a new contacts with a new  document number. And click "confirm tickets"
>    4. Add another new contacts with a different name and same document number. And click "confirm tickets"
>    5. Add another new contacts with a different name and same document number. And click "confirm tickets"
>    6. Only ticket in Step.3 should success and Step4&5 fail because of the duplicate document Number.
        >       But Step4&5 success, this is a fault.
>    7. Find out why and fix it.

#### Notes
1. The code or git branch used in this fault is not the one mentioned in the [fault replication repository](https://github.com/FudanSELab/train-ticket-fault-replicate#f10-ts-error-logic-f10)
   The repository states that **ts-error-logic-f10** should be the correct branch but the code in this branch does not show the expected behaviour.
2. The probably correct branch and code is **ts-error-normal-F10** in the fault replication repository, which is most likely contained in the
   corresponding zip package at https://fudanselab.github.io/research/MSFaultEmpiricalStudy/ (at least the contents of `PreserveOtherServiceImpl`, which is the root cause of the injected error, are identical).

#### Adapted implementation
There is no need to adapt the implementation because the application allows duplicate document ids.
To deactivate this fault the following lines in ``PreserveOtherServiceImpl`` have to be commented in / activated:

```java
/**********If user create a contact with duplicate ID，throw exception***********/
if(oti.getIsCreateContacts().equals("true") && addContactsResult.isExists() == true){
    throw new RuntimeException("[Normal Error] Reproduction Of Error Normal");
}
```

Beware that these are the only lines which have to be commented in / activated, although there are further sections of
commented out code in this file, which might look like they have to be active too.

#### Thoughts
Thinking about the fault, I would expect the application to throw an exception/error when someone creates a contact info
with a duplicate document number. Hence, the actual fault happens when no exception is thrown i.e., when the system does
not prevent duplicate document ids. The description of (ts-error-normal-F10) hints at this behaviour but in combination
with the other descriptions there is room for interpretation. 