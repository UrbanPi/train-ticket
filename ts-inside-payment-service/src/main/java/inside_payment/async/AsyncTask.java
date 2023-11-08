package inside_payment.async;

import java.util.concurrent.Future;

import inside_payment.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component  
public class AsyncTask {  

    @Autowired
	private RestTemplate restTemplate;

    @Async("mySimpleAsync")
    public Future<ModifyOrderStatusResult> sendAsyncCallToModifyOrderStatus(String tripId,String orderId){
        System.out.println("[Inside-Payment][Async][Begin] Send Async Call To Modify Order Status");
        ModifyOrderStatusInfo info = new ModifyOrderStatusInfo();
        info.setOrderId(orderId);
        info.setStatus(1);
        ModifyOrderStatusResult result;
        if(tripId.startsWith("G") || tripId.startsWith("D")){
            result = restTemplate.postForObject(
                    "http://ts-order-service:12031/order/modifyOrderStatus", info, ModifyOrderStatusResult.class);
        }else{
            result = restTemplate.postForObject(
                    "http://ts-order-other-service:12032/orderOther/modifyOrderStatus", info, ModifyOrderStatusResult.class);
        }
        System.out.println("[Inside-Payment][Async][End] Send Async Call To Modify Order Status");
        return new AsyncResult<>(result);
    }

    @Async("mySimpleAsync")
    public Future<GetOrderResult> sendAsyncCallToGetOrder(GetOrderByIdInfo getOrderByIdInfo,String tripId){
        System.out.println("[Inside-Payment][Async][Begin] Send Async Call To Get Order");
        GetOrderResult result;
        if(tripId.startsWith("G") || tripId.startsWith("D")){
            result = restTemplate.postForObject("http://ts-order-service:12031/order/getById",getOrderByIdInfo,GetOrderResult.class);
        }else{
            result = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/getById",getOrderByIdInfo,GetOrderResult.class);
        }
        System.out.println("[Inside-Payment][Async][End] Send Async Call To Get Order");
        return new AsyncResult<>(result);
    }

    @Async("mySimpleAsync")
    public Future<Account> sendAsyncCallToGetAccount(GetAccountByIdInfo info) {
        System.out.println("[Inside-Payment][Async][Begin] Send Async Call To Get Account");
        GetAccountByIdResult result = restTemplate.postForObject("http://ts-sso-service:12349/account/findById", info,GetAccountByIdResult.class);
        if(result.isStatus() == true){
            return new AsyncResult<>(result.getAccount());
        }else{
            return null;
        }
    }
    
}  
