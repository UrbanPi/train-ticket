package ticketinfo.controller;



import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;
import ticketinfo.service.TicketInfoService;

@RestController
public class TicketInfoController {

    @Autowired
    TicketInfoService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Ticket Info Service ] !";
    }

    @RequestMapping(value="/ticketinfo/queryForTravel", method = RequestMethod.POST)
    public ResultForTravel queryForTravel(@RequestBody QueryForTravel info){
        System.out.println("/ticketinfo/queryForTravel");

        return service.queryForTravel(info);
    }

    @RequestMapping(value="/ticketinfo/queryForStationId", method = RequestMethod.POST)
    public String queryForStationId(@RequestBody QueryForStationId info){
        System.out.println("/ticketinfo/queryForStationId");
        return service.queryForStationId(info);
    }
}
