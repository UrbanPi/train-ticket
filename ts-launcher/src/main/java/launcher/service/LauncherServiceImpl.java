package launcher.service;

import launcher.domain.*;
import launcher.task.AsyncTask;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.ArrayList;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.Future;

@Service
public class LauncherServiceImpl implements LauncherService {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private AsyncTask asyncTask;

    public static int count = 0;

    @Override
    public void doErrorQueue(String email,String password){
        //0.Regist
        RegisterInfo registerInfo = new RegisterInfo(email,password);
        RegisterResult registerResult = restTemplate.postForObject(
                "http://ts-register-service:12344/register",
                registerInfo,RegisterResult.class);
        System.out.println("[Register Result] " + registerResult.getMessage());

        //0.1 randomly register for one or two account
        if(new Random().nextBoolean()){
            String randomEmailOne = new Random().nextInt(10000000) + "@fudan.edu.cn";
            RegisterInfo registerInfoExtraOne = new RegisterInfo(randomEmailOne,"passwordpassword");
            RegisterResult registerResultExtraOne = restTemplate.postForObject(
                    "http://ts-register-service:12344/register",
                    registerInfoExtraOne,RegisterResult.class);
            System.out.println("[Random First Account]" + registerResultExtraOne.getMessage());
            if(new Random().nextBoolean()){
                String randomEmailTwo = new Random().nextInt(10000000) + "@fudan.edu.cn";
                RegisterInfo registerInfoExtraTwo = new RegisterInfo(randomEmailTwo,"passwordpassword");
                RegisterResult registerResultExtraTwo = restTemplate.postForObject(
                        "http://ts-register-service:12344/register",
                        registerInfoExtraTwo,RegisterResult.class);
                System.out.println("[Random Second Account]" + registerResultExtraTwo.getMessage());
            }
        }

        //1.login
        LoginInfo loginInfo = new LoginInfo(
                email,
                password,
                "abcd");
        LoginResult loginResult = restTemplate.postForObject(
                "http://ts-login-service:12342/login",
                loginInfo,LoginResult.class
        );
        String loginId = loginResult.getAccount().getId().toString();
        String loginToken = loginResult.getToken();
        System.out.println("[Login Result] " + loginResult.getMessage());

        String orderId = UUID.randomUUID().toString();

        //2.reserve a ticket
        Future<OrderTicketsResult> taskResult = asyncTask.sendOrderTicket(orderId,loginId,loginToken);
        try{
            OrderTicketsResult orderTicketsResult = taskResult.get();
        }catch (Exception e){
            e.printStackTrace();
        }

        //2.pay
        Future<Boolean> payResult  = asyncTask.sendInsidePayment(
                orderId,"Z1234",loginId,loginToken);



        //3.Cancel Order
        Future<CancelOrderResult> taskCancelResult = asyncTask.sendOrderCancel(orderId,loginId,loginToken);


        //4.Search Order twice
        Future<ArrayList<Order>> orderListTask = asyncTask.sendQueryOrder(loginId,loginToken);
        Future<ArrayList<Order>> orderOtherListTask = asyncTask.sendQueryOtherOrder(loginId,loginToken);
        for(;;){
            if(orderListTask.isDone() && orderOtherListTask.isDone()){
                break;
            }
        }


        //5.Whether throws a exception
        try{
            for(;;){
                if(taskCancelResult.isDone()){
                    if(taskCancelResult.get().isStatus() & payResult.get().booleanValue() == false){
                        throw new RuntimeException("[Error Queue]");
                    }else{
                        return;
                    }
                }
            }
        }catch (Exception e){
            e.printStackTrace();
        }

    }

}
