package assurance.controller;

import assurance.domain.*;
import assurance.service.AssuranceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.List;
import java.util.UUID;

@RestController
public class AssuranceController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(AssuranceController.class);

    @Autowired
    private AssuranceService assuranceService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(){
        return "Welcome to [ Assurance Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/findAll", method = RequestMethod.GET)
    public GetAllAssuranceResult getAllAssurances(){
        logger.info("[Assurances Service][Get All Assurances]");
        return assuranceService.getAllAssurances();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/getAllAssuranceType", method = RequestMethod.GET)
    public List<AssuranceTypeBean> getAllAssuranceType(){
        logger.info("[Assurances Service][Get Assurance Type]");
        return assuranceService.getAllAssuranceTypes();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/deleteAssurance", method = RequestMethod.POST)
    public DeleteAssuranceResult deleteAssurance(@RequestParam(value="assuranceId",required = true) String assuranceId){
        logger.info("[Assurances Service][Delete Assurance]");
        return assuranceService.deleteById(UUID.fromString(assuranceId));
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/deleteAssuranceByOrderId", method = RequestMethod.POST)
    public DeleteAssuranceResult deleteAssuranceByOrderId(@RequestParam(value="orderId",required = true) String orderId){
        logger.info("[Assurances Service][Delete Assurance by orderId]");
        return assuranceService.deleteByOrderId(UUID.fromString(orderId));
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/modifyAssurance", method = RequestMethod.POST)
    public ModifyAssuranceResult modifyAssurance(@RequestBody ModifyAssuranceInfo modifyAssuranceInfo){
        logger.info("[Assurances Service][Modify Assurance]");
        return assuranceService.modify(modifyAssuranceInfo);
    }

    ///////////////////////////////////////////////////////////////////////////////////////

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/create", method = RequestMethod.POST)
    public AddAssuranceResult createNewAssurance(@RequestBody AddAssuranceInfo addAssuranceInfo){
//        VerifyResult tokenResult = verifySsoLogin(loginToken);
//        if(tokenResult.isStatus() == true){
//            logger.info("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.create(addAssuranceInfo);
//        }else {
//            logger.info("[AssuranceService][VerifyLogin] Fail.");
//            AddAssuranceResult aar = new AddAssuranceResult();
//            return aar;
//        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/getAssuranceById", method = RequestMethod.GET)
    public Assurance getAssuranceById(@RequestBody GetAssuranceById gabi, @CookieValue String loginId, @CookieValue String loginToken){
//        VerifyResult tokenResult = verifySsoLogin(loginToken);
//        if(tokenResult.isStatus() == true){
//            logger.info("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.findAssuranceById(UUID.fromString(gabi.getAssuranceId()));
//        }else {
//            logger.info("[AssuranceService][VerifyLogin] Fail.");
//            Assurance resultAssurance = new Assurance();
//            return resultAssurance;
//        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/findAssuranceByOrderId", method = RequestMethod.GET)
    public Assurance findAssuranceByOrderId(@RequestBody FindAssuranceByOrderId gabi){
//        VerifyResult tokenResult = verifySsoLogin(gabi.getLoginToken());
//        if(tokenResult.isStatus() == true){
//            logger.info("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.findAssuranceByOrderId(UUID.fromString(gabi.getOrderId()));
//        }else {
//            logger.info("[AssuranceService][VerifyLogin] Fail.");
//            Assurance resultAssurance = new Assurance();
//            return resultAssurance;
//        }
    }

    private VerifyResult verifySsoLogin(String loginToken){
        logger.info("[Assurance Service][Verify Login] Verifying....");
        VerifyResult tokenResult = restTemplate.getForObject(
                "https://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                VerifyResult.class);
        return tokenResult;
    }
}
