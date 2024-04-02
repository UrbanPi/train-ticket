package food.controller;

import food.domain.GetFoodStoresListResult;
import food.domain.GetTrainFoodListResult;
import food.domain.QueryFoodStoresInfo;
import food.domain.QueryTrainFoodInfo;
import food.service.FoodMapService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
public class FoodMapController {
    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(FoodMapController.class);

    @Autowired
    FoodMapService foodMapService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Food Map Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getAllFoodStores", method = RequestMethod.GET)
    public GetFoodStoresListResult getAllFoodStores(){
        logger.info("[Food Map Service][Get All FoodStores]");
        return foodMapService.listFoodStores();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getAllTrainFood", method = RequestMethod.GET)
    public GetTrainFoodListResult getAllTrainFood(){
        logger.info("[Food Map Service][Get All TrainFoods]");
        return foodMapService.listTrainFood();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getFoodStoresOfStation", method = RequestMethod.POST)
    public GetFoodStoresListResult getFoodStoresOfStation(@RequestBody QueryFoodStoresInfo qfs){
        logger.info("[Food Map Service][Get FoodStores By StationId]");
        return foodMapService.listFoodStoresByStationId(qfs.getStationId());
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getTrainFoodOfTrip", method = RequestMethod.POST)
    public GetTrainFoodListResult getTrainFoodOfTrip(@RequestBody QueryTrainFoodInfo qtf){
        logger.info("[Food Map Service][Get TrainFoods By TripId]");
        return foodMapService.listTrainFoodByTripId(qtf.getTripId());
    }


}
