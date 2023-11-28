## ts-error-F16
### Original fault description
> 
> Industrial fault description:
> 
> The file-uploading process fails.
> The "max-content-length" configuration of spray is only 2 Mb, not allowing to support to upload a big file.
> 
> 
> TrainTicket replicated fault description:
> 
> Our system has the ability to add routes in batches. You can upload the file to add routes in batches.
> But the size of the permitted file is too small, sometimes your file will be rejected because of the size.
> 
> 
> 
> 
> Failure Triggering Usage Steps:
> 
> 1. Open the Train-Ticket page and upload a file to add routes in batches whose size is more than 2MB.
> 2. You file will be rejected.


### Notes

Works mostly as described. The default upload limit is 100Kb in `ts-admin-route-service: application.yml`, which causes an 
HTML 500 error. There is a second upload limit of 1MB enforced by `ts-ui-dashboard`, the nginx webserver. This second 
upload limit is the default for the nginx webserver.

In the top level of the there is an example file which can be used for testing. To test the file limit the existing entries
can be copied to inflate the file size. The file contains the following entries:

````csv
shanghai&taiyuan&shanghai,nanjing,shijiazhuang,taiyuan&0,350,1000,1300
shanghai&taiyuan&shanghai,nanjing,shijiazhuang,taiyuan&0,350,1000,1400
shanghai&taiyuan&shanghai,nanjing,shijiazhuang,taiyuan&0,350,1000,1500
shanghai&taiyuan&shanghai,nanjing,shijiazhuang,taiyuan&0,350,1000,1600
shanghai&taiyuan&shanghai,nanjing,shijiazhuang,taiyuan&0,350,1000,1700
````

The difference to the fault implemented in `ts-error-f15` lies in the location where the failure is triggered and 
in the upload limit. In `ts-error-f15` the failure always triggers in `ts-ui-dashboard` (the nginx webserver), in 
`ts-error-f16` it can be triggered by either `ts-ui-dashboard` or `ts-admin-route-service` depending on the file size. 
In both error branches the request triggering the failure is a POST request.

| Error version | Upload limit | Targets                             | Enforced by               |
|---------------|--------------|-------------------------------------|---------------------------|
| ts-error-f15  | 200b         | ts-preserve & ts-preserve-other     | `ts-ui-dashboard`         |
| ts-error-f15  | 1Mb          | default limit applies to all routes | `ts-ui-dashboard`         |
| ts-error-f16  | 1Mb          | default limit applies to all routes | `ts-ui-dashboard`         |
| ts-error-f16  | 100Kb        | ts-admin-route-service              | `ts-admin-route-service`  |
