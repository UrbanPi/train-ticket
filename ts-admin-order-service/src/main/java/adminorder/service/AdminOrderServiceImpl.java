package adminorder.service;

import adminorder.domain.bean.DeleteOrderInfo;
import adminorder.domain.bean.Order;
import adminorder.domain.request.AddOrderRequest;
import adminorder.domain.request.DeleteOrderRequest;
import adminorder.domain.request.UpdateOrderRequest;
import adminorder.domain.response.*;
import com.sun.org.apache.xpath.internal.operations.Bool;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.swing.text.BadLocationException;
import java.util.ArrayList;

@Service
public class AdminOrderServiceImpl implements AdminOrderService {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AdminOrderServiceImpl.class);

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private StringRedisTemplate redisTemplate;

    @Override
    public boolean suspendOrder(String fromStationId,String toStationId){
        logger.info(fromStationId + " " + toStationId);
        restTemplate.getForObject("http://ts-order-other-service:12032/orderOther/suspend/" + fromStationId + "/" + toStationId, Boolean.class);
//        ValueOperations<String, String> ops = redisTemplate.opsForValue();
//        ops.set("adminOrderSuspendFromStationId",fromStationId);
//        ops.set("adminOrderSuspendToStationId",toStationId);
        return true;
    }

    @Override
    public boolean cancelSuspenOrder(String fromStationId,String toStationId){
//        if(redisTemplate.hasKey("adminOrderSuspendFromStationId")){
//            ValueOperations<String, String> ops = redisTemplate.opsForValue();
//            ops.set("adminOrderSuspendFromStationId", "");
//            logger.info("adminOrderSuspendFromStationId 已清空");
//        }else{
//            logger.info("adminOrderSuspendFromStationId 不存在");
//        }
//        if(redisTemplate.hasKey("adminOrderSuspendToStationId")){
//            ValueOperations<String, String> ops = redisTemplate.opsForValue();
//            ops.set("adminOrderSuspendToStationId", "");
//            logger.info("adminOrderSuspendToStationId 已清空");
//        }else{
//            logger.info("adminOrderSuspendToStationId 不存在");
//        }
        logger.info(fromStationId + " " + toStationId);
        restTemplate.getForObject("http://ts-order-other-service:12032//orderOther/cancelSuspend/" + fromStationId + "/" + toStationId, Boolean.class);

        return true;
    }

    @Override
    public GetAllOrderResult getAllOrders(String id) {
        if(checkId(id)){
            logger.info("[Admin Order Service][Get All Orders]");
            //Get all of the orders
            ArrayList<Order> orders = new ArrayList<Order>();
            //From ts-order-service
            QueryOrderResult result = restTemplate.getForObject(
                    "http://ts-order-service:12031/order/findAll",
                    QueryOrderResult.class);
            if(result.isStatus()){
                logger.info("[Admin Order Service][Get Orders From ts-order-service successfully!]");
                orders.addAll(result.getOrders());
            }
            else
                logger.info("[Admin Order Service][Get Orders From ts-order-service fail!]");
            //From ts-order-other-service
            result = restTemplate.getForObject(
                    "http://ts-order-other-service:12032/orderOther/findAll",
                    QueryOrderResult.class);
            if(result.isStatus()){
                logger.info("[Admin Order Service][Get Orders From ts-order-other-service successfully!]");
                orders.addAll(result.getOrders());
            }
            else
                logger.info("[Admin Order Service][Get Orders From ts-order-other-service fail!]");
            //Return orders
            GetAllOrderResult getAllOrderResult = new GetAllOrderResult();
            getAllOrderResult.setStatus(true);
            getAllOrderResult.setMessage("Get the orders successfully!");
            getAllOrderResult.setOrders(orders);
            return getAllOrderResult;
        }
        else{
            logger.info("[Admin Order Service][Wrong Admin ID]");
            GetAllOrderResult result = new GetAllOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + id);
            return result;
        }
    }

    @Override
    public DeleteOrderResult deleteOrder(DeleteOrderRequest request) {
        if(checkId(request.getLoginid())){
            DeleteOrderResult deleteOrderResult = new DeleteOrderResult();

            DeleteOrderInfo deleteOrderInfo = new DeleteOrderInfo();
            deleteOrderInfo.setOrderId(request.getOrderId());

            if(request.getTrainNumber().startsWith("G") || request.getTrainNumber().startsWith("D") ){
                logger.info("[Admin Order Service][Delete Order]");
                deleteOrderResult = restTemplate.postForObject(
                        "http://ts-order-service:12031/order/delete", deleteOrderInfo,DeleteOrderResult.class);
            }
            else{
                logger.info("[Admin Order Service][Delete Order Other]");
                deleteOrderResult = restTemplate.postForObject(
                        "http://ts-order-other-service:12032/orderOther/delete", deleteOrderInfo,DeleteOrderResult.class);
            }
            return deleteOrderResult;
        }
        else{
            logger.info("[Admin Order Service][Wrong Admin ID]");
            DeleteOrderResult result = new DeleteOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
    }

    @Override
    public UpdateOrderResult updateOrder(UpdateOrderRequest request) {
        if(checkId(request.getLoginid())){
            UpdateOrderResult updateOrderResult = new UpdateOrderResult();
            if(request.getOrder().getTrainNumber().startsWith("G") || request.getOrder().getTrainNumber().startsWith("D") ){
                logger.info("[Admin Order Service][Update Order]");
                updateOrderResult = restTemplate.postForObject(
                        "http://ts-order-service:12031/order/adminUpdate", request.getOrder() ,UpdateOrderResult.class);
            }
            else{
                logger.info("[Admin Order Service][Add New Order Other]");
                updateOrderResult = restTemplate.postForObject(
                        "http://ts-order-other-service:12032/orderOther/adminUpdate", request.getOrder() ,UpdateOrderResult.class);
            }
            return updateOrderResult;
        }
        else{
            logger.info("[Admin Order Service][Wrong Admin ID]");
            UpdateOrderResult result = new UpdateOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
    }

    @Override
    public AddOrderResult addOrder(AddOrderRequest request) {
        if(checkId(request.getLoginid())){
            AddOrderResult addOrderResult;
            if(request.getOrder().getTrainNumber().startsWith("G") || request.getOrder().getTrainNumber().startsWith("D") ){
                logger.info("[Admin Order Service][Add New Order]");
                addOrderResult = restTemplate.postForObject(
                        "http://ts-order-service:12031/order/adminAddOrder", request.getOrder() ,AddOrderResult.class);
            }
            else{
                logger.info("[Admin Order Service][Add New Order Other]");
                addOrderResult = restTemplate.postForObject(
                        "http://ts-order-other-service:12032/orderOther/adminAddOrder", request.getOrder() ,AddOrderResult.class);
            }
            return addOrderResult;
        }
        else{
            logger.info("[Admin Order Service][Wrong Admin ID]");
            AddOrderResult result = new AddOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
    }

    private boolean checkId(String id){
        if("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f".equals(id)){
            return true;
        }
        else{
            return false;
        }
    }
}
