package ticketinfo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;


@Service
public class TicketInfoServiceImpl implements TicketInfoService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public ResultForTravel queryForTravel(QueryForTravel info){
//
//        //
//        if(new Random().nextBoolean()){
//            memory();
//        }
//        //


        ResultForTravel result = restTemplate.postForObject(
                "http://ts-basic-service:15680/basic/queryForTravel", info, ResultForTravel.class);
        return result;
    }

    @Override
    public String queryForStationId(QueryForStationId info){
        String id = restTemplate.postForObject(
                "http://ts-basic-service:15680/basic/queryForStationId", info,String.class);
        return id;
    }

//    private void memory() {
//        List<int[]> list = new ArrayList<int[]>();
//
//        Runtime run = Runtime.getRuntime();
//        int i = 1;
//        while (true) {
//            int[] arr = new int[1024 * 8];
//            list.add(arr);
//
//            if (i++ % 1000 == 0) {
//                try {
//                    Thread.sleep(600);
//                } catch (InterruptedException e) {
//                    // TODO Auto-generated catch block
//                    e.printStackTrace();
//                }
//
//                System.out.print("[Order Service]最大内存=" + run.maxMemory() / 1024 / 1024 + "M,");
//                System.out.print("[Order Service]已分配内存=" + run.totalMemory() / 1024 / 1024 + "M,");
//                System.out.print("[Order Service]剩余空间内存=" + run.freeMemory() / 1024 / 1024 + "M");
//                System.out.println(
//                        "[Order Service]最大可用内存=" + (run.maxMemory() - run.totalMemory() + run.freeMemory()) / 1024 / 1024 + "M");
//            }
//        }
//    }
}
