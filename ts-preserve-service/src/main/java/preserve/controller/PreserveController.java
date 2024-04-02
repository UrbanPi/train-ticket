package preserve.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import preserve.domain.*;
import preserve.service.PreserveService;

import java.util.UUID;
import java.util.concurrent.Future;

@RestController
public class PreserveController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(PreserveController.class);

    @Autowired
    private PreserveService preserveService;

    @Autowired
    private StatusBean statusBean;

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/preserve", method = RequestMethod.POST)
    public OrderTicketsResult preserve(@RequestBody OrderTicketsInfoPlus otiPlus, @CookieValue String loginToken) throws Exception {

        OrderTicketsInfo oti = otiPlus.getInfo();

        String loginId = otiPlus.getLoginId();


        logger.info("[Preserve Service][Preserve] Account " + loginId + " order from " +
                oti.getFrom() + " -----> " + oti.getTo() + " at " + oti.getDate());

        //add this request to the queue of requests
        UUID uuid = UUID.randomUUID();
        PreserveNode pn = new PreserveNode(uuid, loginId);
        statusBean.chartMsgs.add(pn);

        Future<OrderTicketsResult> otr = preserveService.preserve(oti,loginId,loginToken);
        //wait the task done
        while(true) {
            if(otr.isDone()) {
                logger.info("------preserveService uuid = " + uuid  +  " done--------");
                break;
            }
            Thread.sleep(300);
        }

        OrderTicketsResult result = otr.get();
        int index = statusBean.chartMsgs.indexOf(pn);
        //some error happened that beyond image
        if(index < 0){
            statusBean.chartMsgs.remove(pn);
            logger.info("-----cannot find the current preserve node.------");
            throw new Exception("cannot find the current preserve node.");
        } else {
            //check if there exists any request from the same loginId that haven't return
            for(int i = 0; i < index; i++){
                if(statusBean.chartMsgs.get(i).getLoginId().equals(loginId)){
                    statusBean.chartMsgs.remove(pn);
                    logger.info("-----This OrderTicketsResult return before the last loginId request.------");
                    result.setStatus(false);
                    result.setMessage("ErrorReportUI");
                    return result;
                    //throw new Exception("This OrderTicketsResult return before the last loginId request.");
                }
            }
        }

        logger.info("-----This OrderTicketsResult return in the sequence.------");
        statusBean.chartMsgs.remove(pn);

        return result;
    }


}
