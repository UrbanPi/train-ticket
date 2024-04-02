package click.controller;

import click.async.AsyncTask;
import click.domain.OrderTicketsInfo;
import click.domain.OrderTicketsResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.concurrent.Future;

@RestController
public class ClickController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(ClickController.class);

    @Autowired
    private AsyncTask asyncTask;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to Click ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/click/clickTwice", method = RequestMethod.POST)
    public OrderTicketsResult clickTwice(@RequestBody OrderTicketsInfo oti, @CookieValue String loginId, @CookieValue String loginToken) throws Exception{
        logger.info("Click Two");
        Future<OrderTicketsResult> task1 = asyncTask.sendAsyncClickTwice(oti,loginId,loginToken);
        Thread.sleep(500);
        Future<OrderTicketsResult> task2 = asyncTask.sendAsyncClickTwice(oti,loginId,loginToken);
        while(!(task1.isDone() && task2.isDone())){

        }
        OrderTicketsResult result1 = task1.get();
        OrderTicketsResult result2 = task2.get();
        if(result1.getMessage().contains("ErrorReportUI") || result2.getMessage().contains("ErrorReportUI")){
            throw new Exception("This OrderTicketsResult return before the last loginId request.");
        }else{
            return result1;

        }
    }

}
