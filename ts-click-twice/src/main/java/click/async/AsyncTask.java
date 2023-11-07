package click.async;

import click.domain.OrderTicketsInfo;
import click.domain.OrderTicketsInfoPlus;
import click.domain.OrderTicketsResult;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import java.util.concurrent.Future;

@Component  
public class AsyncTask {
    @Autowired
	private RestTemplate restTemplate;

    @Async("myAsync")
    public Future<OrderTicketsResult> sendAsyncClickTwice(OrderTicketsInfo info,String loginId, String loginToken) throws InterruptedException {



        OrderTicketsInfoPlus plus = new OrderTicketsInfoPlus();
        plus.setInfo(info);
        plus.setLoginId(loginId);
        plus.setLoginToken(loginToken);

        OrderTicketsResult result = restTemplate.postForObject("http://ts-preserve-service:14568/preserve",plus,OrderTicketsResult.class);

        return new AsyncResult<>(result);

    }

      
}  
