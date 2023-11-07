package fdse.microservice.controller;

import fdse.microservice.domain.QueryForTravel;
import fdse.microservice.domain.QueryStation;
import fdse.microservice.domain.ResultForTravel;
import fdse.microservice.service.BasicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


@RestController
public class BasicController {

    @Autowired
    BasicService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Basic Info Service ] !";
    }

    @RequestMapping(value="/basic/queryForTravel", method= RequestMethod.POST)
    public ResultForTravel queryForTravel(@RequestBody QueryForTravel info){
        System.out.println("/basic/queryForTravel");
        return service.queryForTravel(info);
    }

    @RequestMapping(value="/basic/queryForStationId", method= RequestMethod.POST)
    public String queryForStationId(@RequestBody QueryStation info){
        System.out.println("/basic/queryForStationId");
        return service.queryForStationId(info);
    }
}
