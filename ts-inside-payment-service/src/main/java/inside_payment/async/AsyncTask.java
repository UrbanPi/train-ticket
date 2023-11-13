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
    
    @Autowired
	private RestTemplate restTemplate;

    @Async("mySimpleAsync")
    public Future<Boolean> sendAsyncCallToPaymentService(OutsidePaymentInfo outsidePaymentInfo) throws InterruptedException{
        System.out.println("[Inside Payment Service][Async Task] Begin.");
        Boolean value = restTemplate.getForObject("http://rest-service-external:16100/greet", Boolean.class);
        System.out.println("[Inside Payment Service][Async Task] Value:" + value);
        return new AsyncResult<>(value);
    }
    
}  
