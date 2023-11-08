package click.controller;

import click.async.AsyncTask;
import click.domain.LoginInfo;
import click.domain.LoginResult;
import click.domain.OrderTicketsResult;
import click.domain.TravelAdvanceResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Random;
import java.util.concurrent.Future;

@RestController
public class ClickController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private AsyncTask asyncTask;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to auto ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/click/occupy", method = RequestMethod.GET)
    public boolean occupy() throws Exception {
        //登录
        String email = "fdse_microservices@163.com";
        String password = "DefaultPassword";
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

        //点2次确认车票，并等待结果
        for(int i = 0;i < 6;i++){
            Future<TravelAdvanceResult> taskResult = asyncTask.searchInAdvanceSearch(loginId,loginToken);
        }
        return true;
    }


    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/click/auto", method = RequestMethod.GET)
    public boolean autoFail() throws Exception{
        //登录
        String email = "fdse_microservices@163.com";
        String password = "DefaultPassword";
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


        for(int i = 0;i < 1;i++){
            Future<TravelAdvanceResult> taskResult = asyncTask.searchInAdvanceSearch(loginId,loginToken);
        }
        return false;
    }

}
