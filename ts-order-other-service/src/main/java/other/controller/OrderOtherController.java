package other.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import other.domain.*;
import other.repository.OrderOtherRepository;
import other.service.OrderOtherService;

import java.util.ArrayList;

@RestController
public class OrderOtherController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(OrderOtherController.class);

    @Autowired
    private OrderOtherService orderService;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private OrderOtherRepository orderOtherRepository;



    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Order Other Service ] !";
    }

    @RequestMapping(path = "/getStatusDescription", method = RequestMethod.GET)
    public String getStatusDescription() {
        return orderService.getStatusDescription();
    }


    /***************************For Normal Use***************************/

    @RequestMapping(value = "/orderOther/suspend/{fromId}/{toId}", method = RequestMethod.GET)
    public Boolean setSuspendStation(@PathVariable String fromId, @PathVariable String toId){
        return new Boolean(orderService.suspend(fromId,toId));
    }

    @RequestMapping(value = "/orderOther/cancelSuspend/{fromId}/{toId}", method = RequestMethod.GET)
    public Boolean setCancelSuspendStation(@PathVariable String fromId, @PathVariable String toId){
        return new Boolean(orderService.cancelSuspend(fromId,toId));
    }

    @RequestMapping(value = "/orderOther/getSuspendStationArea", method = RequestMethod.GET)
    public SuspendArea getSuspendStationArea(){
        logger.info("[Order Other Service] Get Suspend Station Area.");
        return orderService.getSuspendArea();
    }


    @RequestMapping(value = "/orderOther/getOrdersByFromAndTo/{fromId}/{toId}", method = RequestMethod.GET)
    public ArrayList<Order> getOrdersByFromIdAndToId(@PathVariable String fromId, @PathVariable String toId){

        logger.info("[Order Service][Get] From:" + fromId + " To:" + toId);

        ArrayList<Order> ordersFrom = orderOtherRepository.findByFromId(fromId);
        ArrayList<Order> ordersTo = orderOtherRepository.findByToId(toId);

        ArrayList<Order> orders = new ArrayList<>();
        orders.addAll(ordersFrom);
        orders.addAll(ordersTo);

        logger.info("[Order Service][Get] From:" + ordersFrom.size() + " To:" + ordersTo.size());

        return orders;
    }

    @RequestMapping(value="/orderOther/getTicketListByDateAndTripId", method = RequestMethod.POST)
    public LeftTicketInfo getTicketListByDateAndTripId(@RequestBody SeatRequest seatRequest){

        logger.info("[Order Other Service][Get Sold Ticket] Date:" + seatRequest.getTravelDate().toString());
        LeftTicketInfo leftTicketInfo = orderService.getSoldTickets(seatRequest);;

        return leftTicketInfo;

    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/asyncViewAllOrder", method = RequestMethod.GET)
    public QueryOrderResult asyncViewAllOrder(){
        return orderService.getAllOrdersAsync();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/create", method = RequestMethod.POST)
    public CreateOrderResult createNewOrder(@RequestBody CreateOrderInfo coi,@CookieValue String loginToken){

        logger.info("[Order Other Service][Create Order] Create Order form " + coi.getOrder().getFrom() + " --->"
                + coi.getOrder().getTo() + " at " + coi.getOrder().getTravelDate());
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        CreateOrderResult createOrderResult;
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            createOrderResult = orderService.create(coi.getOrder());
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            CreateOrderResult cor = new CreateOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            createOrderResult = cor;
        }

        return createOrderResult;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminAddOrder", method = RequestMethod.POST)
    public AddOrderResult addcreateNewOrder(@RequestBody Order order){

        AddOrderResult addOrderResult = orderService.addNewOrder(order);

        return addOrderResult;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/query", method = RequestMethod.POST)
    public ArrayList<Order> queryOrders(@RequestBody QueryInfo qi,@CookieValue String loginId,@CookieValue String loginToken){

        logger.info("[Order Other Service][Query Orders] Query Orders for " + loginId);
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        ArrayList<Order> orders;
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            orders = orderService.queryOrders(qi,loginId);
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            orders = new ArrayList<>();
        }

        return orders;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/calculate", method = RequestMethod.POST)
    public CalculateSoldTicketResult calculateSoldTicket(@RequestBody CalculateSoldTicketInfo csti){

        logger.info("[Order Other Service][Calculate Sold Tickets] Date:" + csti.getTravelDate() + " TrainNumber:"
                + csti.getTrainNumber());
        CalculateSoldTicketResult result = orderService.queryAlreadySoldOrders(csti);

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/price", method = RequestMethod.POST)
    public GetOrderPriceResult getOrderPrice(@RequestBody GetOrderPrice info){

        logger.info("[Order Other Service][Get Order Price] Order Id:" + info.getOrderId());
        GetOrderPriceResult result = orderService.getOrderPrice(info);

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/payOrder", method = RequestMethod.POST)
    public PayOrderResult payOrder(@RequestBody PayOrderInfo info){

        logger.info("[Order Other Service][Pay Order] Order Id:" + info.getOrderId());
        PayOrderResult result = orderService.payOrder(info);

        return result;

    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/getById", method = RequestMethod.POST)
    public GetOrderResult getOrderById(@RequestBody GetOrderByIdInfo info){

        logger.info("[Order Other Service][Get Order By Id] Order Id:" + info.getOrderId());
        GetOrderResult result = orderService.getOrderById(info);

        return result;

    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/modifyOrderStatus", method = RequestMethod.POST)
    public ModifyOrderStatusResult modifyOrder(@RequestBody ModifyOrderStatusInfo info){

        logger.info("[Order Other Service][Modify Order Status] Order Id:" + info.getOrderId());
        ModifyOrderStatusResult result = orderService.modifyOrder(info);

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/getOrderOtherInfoForSecurity", method = RequestMethod.POST)
    public GetOrderInfoForSecurityResult securityInfoCheck(@RequestBody GetOrderInfoForSecurity info){

        logger.info("[Order Other Service][Security Info Get]");
        GetOrderInfoForSecurityResult result = orderService.checkSecurityAboutOrder(info);

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/update", method = RequestMethod.POST)
    public ChangeOrderResult saveOrderInfo(@RequestBody ChangeOrderInfo orderInfo,@CookieValue String loginToken){

        ChangeOrderResult result;
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            result =  orderService.saveChanges(orderInfo.getOrder());
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            ChangeOrderResult cor = new ChangeOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            result = cor;
        }

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminUpdate", method = RequestMethod.POST)
    public UpdateOrderResult updateOrder(@RequestBody Order order){

        UpdateOrderResult result = orderService.updateOrder(order);

        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/delete",method = RequestMethod.POST)
    public DeleteOrderResult deleteOrder(@RequestBody DeleteOrderInfo info){

        logger.info("[Order Other Service][Delete Order] Order Id:" + info.getOrderId());
        DeleteOrderResult result = orderService.deleteOrder(info);

        return result;
    }


    /***************For super admin(Single Service Test*******************/

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/findAll", method = RequestMethod.GET)
    public QueryOrderResult findAllOrder(){

        logger.info("[Order Other Service][Find All Order]");
        QueryOrderResult result = orderService.getAllOrders();

        return result;
    }

    private VerifyResult verifySsoLogin(String loginToken){
        logger.info("[Order Other Service][Verify Login] Verifying....");
        VerifyResult tokenResult = restTemplate.getForObject(
                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                VerifyResult.class);
        return tokenResult;
    }
}
