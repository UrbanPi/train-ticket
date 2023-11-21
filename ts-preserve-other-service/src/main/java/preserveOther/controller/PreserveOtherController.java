package preserveOther.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import preserveOther.domain.OrderTicketsInfo;
import preserveOther.domain.OrderTicketsInfoWithOrderId;
import preserveOther.domain.OrderTicketsResult;
import preserveOther.service.PreserveOtherService;

@RestController
public class PreserveOtherController {

    @Autowired
    private PreserveOtherService preserveService;

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/preserveOther", method = RequestMethod.POST)
    public OrderTicketsResult preserve(@RequestBody OrderTicketsInfoWithOrderId oti, @CookieValue String loginId, @CookieValue String loginToken){
        System.out.println("[Preserve Other Service][Preserve] Account " + loginId + " order from " +
                oti.getFrom() + " -----> " + oti.getTo() + " at " + oti.getDate());
        return preserveService.preserve(oti,loginId,loginToken);
    }
}
