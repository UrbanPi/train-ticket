package click.async;

import click.domain.OrderTicketsInfo;
import click.domain.OrderTicketsResult;
import click.domain.QueryInfo;
import click.domain.TravelAdvanceResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.Future;

@Component  
public class AsyncTask {
    @Autowired
	private RestTemplate restTemplate;

    @Async("mySimpleAsync")
    public Future<OrderTicketsResult> sendOrderTicket(String loginId, String loginToken){

        OrderTicketsInfo orderTicketsInfo = new OrderTicketsInfo();
        orderTicketsInfo.setContactsId("4d2a46c7-71cb-4cf1-a5bb-b68406d9da6f");
        orderTicketsInfo.setTripId("Z1234");
        orderTicketsInfo.setSeatType(2);
        orderTicketsInfo.setDate(new Date(1504137600000L));
        orderTicketsInfo.setFrom("Shang Hai");
        orderTicketsInfo.setTo("Nan Jing");

        HttpHeaders requestHeadersPreserveOrder = new HttpHeaders();
        requestHeadersPreserveOrder.add("Cookie","loginId=" + loginId);
        requestHeadersPreserveOrder.add("Cookie","loginToken=" + loginToken);
        HttpEntity< OrderTicketsInfo> requestEntityPreserveOrder = new HttpEntity( orderTicketsInfo, requestHeadersPreserveOrder);
        ResponseEntity rssResponsePreserveOrder = restTemplate.exchange(
                "http://ts-preserve-other-service:14569/preserveOther",
                HttpMethod.POST, requestEntityPreserveOrder, OrderTicketsResult.class);
        OrderTicketsResult orderTicketsResult = (OrderTicketsResult)rssResponsePreserveOrder.getBody();

        if(orderTicketsResult == null){
            throw new RuntimeException("Error");
        }

        System.out.println("[预定结果] " + orderTicketsResult.getMessage());
        return new AsyncResult(orderTicketsResult);
    }

    @Async("mySimpleAsync")
    public Future<TravelAdvanceResult> searchInAdvanceSearch(String loginId, String loginToken) throws Exception{

        QueryInfo getRoutePlanInfo = new QueryInfo();
        getRoutePlanInfo.setStartingPlace("Shang Hai");
        getRoutePlanInfo.setEndPlace("Nan Jing");

        java.text.SimpleDateFormat formatter = new SimpleDateFormat( "yyyy-MM-dd");
        String s = "2020-12-12";
        Date date = formatter.parse(s);

        //date = new Date(1504137600000L);

        getRoutePlanInfo.setDepartureTime(date);

        TravelAdvanceResult results = restTemplate.postForObject(
                "http://ts-travel-plan-service:14322/travelPlan/getCheapest",
                getRoutePlanInfo,TravelAdvanceResult.class);

        if(results == null){
            throw new RuntimeException("Error");
        }

        System.out.println("[搜索结果]" + results.isStatus() + " " + results.getTravelAdvanceResultUnits().size());

        return null;
    }
      
}  
