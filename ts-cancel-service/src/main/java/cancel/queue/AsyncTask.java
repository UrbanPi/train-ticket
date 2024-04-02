package cancel.queue;

import cancel.domain.ChangeOrderInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component  
public class AsyncTask {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AsyncTask.class);

    @Autowired
    private MsgSendingBean sendingBean;

    @Async("mySimpleAsync")
    public void asyncSendLoginInfoDataToSso(ChangeOrderInfo info){
        logger.info("[Cancel Service][Async Send Login Info]");
        sendingBean.sendCancelInfoToOrderOther(info);
    }
      
}  
