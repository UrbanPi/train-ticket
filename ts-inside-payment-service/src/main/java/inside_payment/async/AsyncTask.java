package inside_payment.async;

import java.util.concurrent.Future;
import inside_payment.domain.OutsidePaymentInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component  
public class AsyncTask {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AsyncTask.class);
    
    @Autowired
	private RestTemplate restTemplate;

    @Async("mySimpleAsync")
    public Future<Boolean> sendAsyncCallToPaymentService(OutsidePaymentInfo outsidePaymentInfo) throws InterruptedException{
        logger.info("[Inside Payment Service][Async Task] Begin.");
        Boolean value = restTemplate.getForObject("http://ts-rest-external-service:16100/greet", Boolean.class);
        logger.info("[Inside Payment Service][Async Task] Value:" + value);
        return new AsyncResult<>(value);
    }
    
}  
