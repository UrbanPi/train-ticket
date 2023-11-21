package cancel.async;

import java.util.concurrent.Future;
import cancel.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;


/** 
 * Asynchronous Tasks 
 * @author Xu 
 * 
 */  
@Component  
public class AsyncTask {
    
    @Autowired
	private RestTemplate restTemplate;

    @Async("myAsync")
    public Future<ChangeOrderResult> updateOtherOrderStatusToCancel(ChangeOrderInfo info) throws InterruptedException{

        Thread.sleep(2000);

        System.out.println("[Cancel Order Service][Change Order Status] Getting....");
        ChangeOrderResult result = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/update",info,ChangeOrderResult.class);
        return new AsyncResult<>(result);
    }


    @Async("mySimpleAsync")
    public Future<ChangeOrderResult> cancelling(String userId,String orderId,String loginToken) throws InterruptedException{

        if(Math.random() < 0.6){
            Thread.sleep(4000);
        }

        //1.查询订单信息
        GetOrderByIdInfo getOrderInfo = new GetOrderByIdInfo();
        getOrderInfo.setOrderId(orderId);
        GetOrderResult cor = restTemplate.postForObject(
                "http://ts-order-other-service:12032/orderOther/getById/"
                ,getOrderInfo,GetOrderResult.class);
        Order order = cor.getOrder();

        //2.将订单状态修改为退款中
        order.setStatus(OrderStatus.Canceling.getCode());
        ChangeOrderInfo changeOrderInfo = new ChangeOrderInfo();
        changeOrderInfo.setOrder(order);
        changeOrderInfo.setLoginToken(loginToken);
        ChangeOrderResult changeOrderResult = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/update",changeOrderInfo,ChangeOrderResult.class);

        return new AsyncResult<>(changeOrderResult);
    }


    @Async("mySimpleAsync")
    public Future<Boolean> drawBackMoney(String money, String userId,String orderId,String loginToken) throws InterruptedException{
        Thread.sleep(2000);
        //3.执行退款
        DrawBackInfo info = new DrawBackInfo();
        info.setMoney(money);
        info.setUserId(userId);
        info.setOrderId(orderId);
        info.setLoginToken(loginToken);
        String result = restTemplate.postForObject("http://ts-inside-payment-service:18673/inside_payment/drawBack",info,String.class);
        if(result.equals("true")){
            return new AsyncResult<>(true);
        }else{
            return new AsyncResult<>(false);
        }
    }
      
}  
