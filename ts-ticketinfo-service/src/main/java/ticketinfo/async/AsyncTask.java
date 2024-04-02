package ticketinfo.async;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;

import java.util.concurrent.Future;

@Component  
public class AsyncTask {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AsyncTask.class);  

    @Autowired
	private RestTemplate restTemplate;

    public static int size;

    @Async("mySimpleAsync")
    public Future<ResultForTravel> queryForTravel(QueryForTravel info){
        size += 1;
        logger.info("[Ticket Info] Thread Size: " + size);
        ResultForTravel result = restTemplate.postForObject(
                "http://ts-basic-service:15680/basic/queryForTravel", info, ResultForTravel.class);
        size -= 1;
        return new AsyncResult<>(result);
    }

}  
