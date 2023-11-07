# Setup System#
   mvn clean package
   docker-compose build
   docker-compose up
 
# Replicate The Fault
Step 1:
    Login
Step 2:
    Search for a ticket using the following info:
        Starting Place: Shang Hai
        Terminal Place: Su hou
        Date: After today
        Train Type: GaoTie DongChe
Step 3:
    Click [Booking]
Step 4:
    Click [Refresh Contacts]
    Select one of the Contacts and click [Select]
Step 5: 
    Click [Confirm Ticket]
    You may try some more times if you get a "Success". If the fault occurs, you will get an [Error] and you
    will see the exception logs in console.  

# Tip
   In order to simplify the process of log collection, we add a service name click-twice.
   If you click [Confirm Ticket], a request will be sent to click-twice, and this service will send two
request to ticket-preserve asynchronous. In some cases the fault will occurs.
  
# How the fault occurs
1. In [ts-preserve-service] -> [PreserController], a var named [statusBean] will save the unfinished request.
2. In [ts-preserve-service] -> [PreserviceImpl] -> [preserve], a random delay is added at the beginning of this method.
3. For a user who send 2 requests to [ts-preservice-service] in a short time, the 2nd request may be finished early before the first one due to the random delay.
   In such situation, the system will found that this user has a non-finished request which should be finished before the 2nd request.
   Then the exception will be thrown.
        

        
