package preserve.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import preserve.domain.*;
import preserve.service.PreserveService;

@RestController
public class PreserveController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(PreserveController.class);

    @Autowired
    private PreserveService preserveService;

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/preserve", method = RequestMethod.POST)
    public OrderTicketsResult preserve(@RequestBody OrderTicketsInfo oti,@CookieValue String loginId,@CookieValue String loginToken){
        logger.info("[Preserve Service][Preserve] Account " + loginId + " order from " +
            oti.getFrom() + " -----> " + oti.getTo() + " at " + oti.getDate());
        return preserveService.preserve(oti,loginId,loginToken);
    }

}
