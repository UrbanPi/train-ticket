package ticketinfo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import ticketinfo.async.AsyncTask;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;

import java.util.concurrent.TimeUnit;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
@Service
public class TicketInfoServiceImpl implements TicketInfoService{

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private AsyncTask asyncTask;

    @Override
    public ResultForTravel queryForTravel(QueryForTravel info){
//        ResultForTravel result = restTemplate.postForObject(
//                "http://ts-basic-service:15680/basic/queryForTravel", info, ResultForTravel.class);
//        return result;
        try{
            return asyncTask.queryForTravel(info).get(20000, TimeUnit.MILLISECONDS);
        }catch(Exception e){
            //e.printStackTrace();
            return null;
        }

    }

    @Override
    public String queryForStationId(QueryForStationId info){
        String id = restTemplate.postForObject(
                "http://ts-basic-service:15680/basic/queryForStationId", info,String.class);
        return id;
    }
}
