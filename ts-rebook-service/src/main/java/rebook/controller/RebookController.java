package rebook.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import rebook.domain.RebookInfo;
import rebook.domain.RebookResult;
import rebook.service.RebookService;

@RestController
public class RebookController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(RebookController.class);

    @Autowired
    RebookService service;

    @RequestMapping(value="/rebook/payDifference", method = RequestMethod.POST)
    public RebookResult payDifference(@RequestBody RebookInfo info, @CookieValue String loginId, @CookieValue String loginToken){
        return service.payDifference(info, loginId, loginToken);
    }

    @RequestMapping(value="/rebook/rebook", method = RequestMethod.POST)
    public RebookResult rebook(@RequestBody RebookInfo info, @CookieValue String loginId, @CookieValue String loginToken){
        logger.info("[Rebook Service] OrderId:" + info.getOrderId() + "Old Trip Id:" + info.getOldTripId() + " New Trip Id:" + info.getTripId() + " Date:" + info.getDate() + " Seat Type:" + info.getSeatType());
        return service.rebook(info, loginId, loginToken);
    }
}
