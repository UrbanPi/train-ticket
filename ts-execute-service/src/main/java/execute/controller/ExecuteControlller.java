package execute.controller;

import execute.domain.TicketExecuteInfo;
import execute.domain.TicketExecuteResult;
import execute.serivce.ExecuteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class ExecuteControlller {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(ExecuteControlller.class);

    @Autowired
    private ExecuteService executeService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Execute Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/execute/execute", method = RequestMethod.POST)
    public TicketExecuteResult executeTicket(@RequestBody TicketExecuteInfo info){
        logger.info("[Execute Service][Execute] Id:" + info.getOrderId());
        return executeService.ticketExecute(info);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/execute/collected", method = RequestMethod.POST)
    public TicketExecuteResult collectTicket(@RequestBody TicketExecuteInfo info){
        logger.info("[Execute Service][Collect] Id:" + info.getOrderId());
        return executeService.ticketCollect(info);
    }
}
