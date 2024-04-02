package other.queue;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import other.domain.ChangeOrderInfo;
import other.domain.ChangeOrderResult;
import other.service.OrderOtherService;

@Component  
public class AsyncTask {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AsyncTask.class);

    @Autowired
    private MsgSendingBean sendingBean;

    @Autowired
    private OrderOtherService service;

    @Async("mySimpleAsync")
    public void putResultIntoReturnQueue(ChangeOrderInfo changeOrderInfo){
        //1.调用service进行执行执行
        logger.info("[Order Other Service][Async Task] 准备开始修改状态");
        ChangeOrderResult changeOrderResult = service.saveChanges(changeOrderInfo.getOrder());
        //2.获取result
        sendingBean.sendLoginInfoToSso(changeOrderResult);

    }
      
}  
