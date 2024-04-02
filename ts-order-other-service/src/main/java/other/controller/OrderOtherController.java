package other.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import other.domain.*;
import other.service.OrderOtherService;
import java.util.ArrayList;

@RestController
public class OrderOtherController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(OrderOtherController.class);

    @Autowired
    private OrderOtherService orderService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Order Other Service ] !";
    }

    /***************************For Normal Use***************************/

    @RequestMapping(value="/orderOther/getTicketListByDateAndTripId", method = RequestMethod.POST)
    public LeftTicketInfo getTicketListByDateAndTripId(@RequestBody SeatRequest seatRequest){
        logger.info("[Order Other Service][Get Sold Ticket] Date:" + seatRequest.getTravelDate().toString());
        return orderService.getSoldTickets(seatRequest);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/create", method = RequestMethod.POST)
    public CreateOrderResult createNewOrder(@RequestBody CreateOrderInfo coi,@CookieValue String loginToken){
        logger.info("[Order Other Service][Create Order] Create Order form " + coi.getOrder().getFrom() + " --->"
                + coi.getOrder().getTo() + " at " + coi.getOrder().getTravelDate());
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            return orderService.create(coi.getOrder());
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            CreateOrderResult cor = new CreateOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            return cor;
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminAddOrder", method = RequestMethod.POST)
    public AddOrderResult addcreateNewOrder(@RequestBody Order order){
        return orderService.addNewOrder(order);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/query", method = RequestMethod.POST)
    public ArrayList<Order> queryOrders(@RequestBody QueryInfo qi,@CookieValue String loginId,@CookieValue String loginToken){
        logger.info("[Order Other Service][Query Orders] Query Orders for " + loginId);
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            return orderService.queryOrders(qi,loginId);
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            return new ArrayList<Order>();
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/calculate", method = RequestMethod.POST)
    public CalculateSoldTicketResult calculateSoldTicket(@RequestBody CalculateSoldTicketInfo csti){
        logger.info("[Order Other Service][Calculate Sold Tickets] Date:" + csti.getTravelDate() + " TrainNumber:"
                + csti.getTrainNumber());
        return orderService.queryAlreadySoldOrders(csti);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/price", method = RequestMethod.POST)
    public GetOrderPriceResult getOrderPrice(@RequestBody GetOrderPrice info){
        logger.info("[Order Other Service][Get Order Price] Order Id:" + info.getOrderId());
        return orderService.getOrderPrice(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/payOrder", method = RequestMethod.POST)
    public PayOrderResult payOrder(@RequestBody PayOrderInfo info){
        logger.info("[Order Other Service][Pay Order] Order Id:" + info.getOrderId());
        return orderService.payOrder(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/getById", method = RequestMethod.POST)
    public GetOrderResult getOrderById(@RequestBody GetOrderByIdInfo info){
        logger.info("[Order Other Service][Get Order By Id] Order Id:" + info.getOrderId());
        return orderService.getOrderById(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/modifyOrderStatus", method = RequestMethod.POST)
    public ModifyOrderStatusResult modifyOrder(@RequestBody ModifyOrderStatusInfo info){
        logger.info("[Order Other Service][Modify Order Status] Order Id:" + info.getOrderId());
        return orderService.modifyOrder(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/getOrderOtherInfoForSecurity", method = RequestMethod.POST)
    public GetOrderInfoForSecurityResult securityInfoCheck(@RequestBody GetOrderInfoForSecurity info){
        logger.info("[Order Other Service][Security Info Get]");
        return orderService.checkSecurityAboutOrder(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/update", method = RequestMethod.POST)
    public ChangeOrderResult saveOrderInfo(@RequestBody ChangeOrderInfo orderInfo,@CookieValue String loginToken){
        VerifyResult tokenResult = verifySsoLogin(loginToken);
        if(tokenResult.isStatus() == true){
            logger.info("[Order Other Service][Verify Login] Success");
            return orderService.saveChanges(orderInfo.getOrder());
        }else{
            logger.info("[Order Other Service][Verify Login] Fail");
            ChangeOrderResult cor = new ChangeOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            return cor;
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminUpdate", method = RequestMethod.POST)
    public UpdateOrderResult updateOrder(@RequestBody Order order){
        return orderService.updateOrder(order);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/delete",method = RequestMethod.POST)
    public DeleteOrderResult deleteOrder(@RequestBody DeleteOrderInfo info){
        logger.info("[Order Other Service][Delete Order] Order Id:" + info.getOrderId());
        return orderService.deleteOrder(info);
    }


    /***************For super admin(Single Service Test*******************/

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/findAll", method = RequestMethod.GET)
    public QueryOrderResult findAllOrder(){
        logger.info("[Order Other Service][Find All Order]");
        return orderService.getAllOrders();
    }

    private VerifyResult verifySsoLogin(String loginToken){
        logger.info("[Order Other Service][Verify Login] Verifying....");
        VerifyResult tokenResult = restTemplate.getForObject(
                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                VerifyResult.class);
        return tokenResult;
    }
}
