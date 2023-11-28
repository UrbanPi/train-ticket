package adminroute.controller;

import adminroute.domain.bean.CreateAndModifyRouteInfo;
import adminroute.domain.request.CreateAndModifyRouteRequest;
import adminroute.domain.request.DeleteRouteRequest;
import adminroute.domain.response.CreateAndModifyRouteResult;
import adminroute.domain.response.DeleteRouteResult;
import adminroute.domain.response.GetRoutesListlResult;
import adminroute.service.AdminRouteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.util.UUID;

@RestController
public class AdminRouteController {
    @Autowired
    AdminRouteService adminRouteService;

    @Autowired
    private RestTemplate restTemplate;


    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminroute/findAll", method = RequestMethod.POST)
    public void addRouteSet(){

    }


    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminroute/findAll/{id}", method = RequestMethod.GET)
    public GetRoutesListlResult getAllRoutes(@PathVariable String id){
        return adminRouteService.getAllRoutes(id);
    }

    @RequestMapping(value = "/adminroute/createAndModifyRoute", method= RequestMethod.POST)
    public CreateAndModifyRouteResult addRoute(@RequestBody CreateAndModifyRouteRequest request){
        return adminRouteService.createAndModifyRoute(request);
    }

    @RequestMapping(value = "/adminroute/deleteRoute", method= RequestMethod.POST)
    public DeleteRouteResult deleteRoute(@RequestBody DeleteRouteRequest request){
        return adminRouteService.deleteRoute(request);
    }

    @RequestMapping(value = "/adminroute/upload", method = RequestMethod.POST)
    @ResponseBody
    public String upload(@RequestParam("file") MultipartFile file) {

        if (!file.isEmpty()) {
            try {

                System.out.println("File Upload - File Name: " + file.getName());
                System.out.println("File Upload - File Original Filename" + file.getOriginalFilename());
                System.out.println("File Upload - File Size" + file.getSize());

                BufferedOutputStream out = new BufferedOutputStream(
                        new FileOutputStream(new File(file.getOriginalFilename())));
                out.write(file.getBytes());
                out.flush();
                out.close();

                FileInputStream inputStream = new FileInputStream(file.getOriginalFilename());
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

                String str = null;
                while((str = bufferedReader.readLine()) != null) {
                    System.out.println("[Upload Read Line]" + str);

                    String[] strList = str.split("&");

                    if(strList.length != 4){
                        System.out.println("[Array Length]：" + strList.length);
                        continue;
                    }

                    String startStationId = strList[0];
                    String endStationId = strList[1];
                    String stationListStr = strList[2];
                    String distanceList = strList[3];

                    CreateAndModifyRouteInfo info = new CreateAndModifyRouteInfo();
                    info.setId("");
                    info.setStartStation(startStationId);
                    info.setEndStation(endStationId);
                    info.setStationList(stationListStr);
                    info.setDistanceList(distanceList);
                    CreateAndModifyRouteResult result = restTemplate.postForObject(
                            "http://ts-route-service:11178/route/createAndModify",
                            info, CreateAndModifyRouteResult.class);
                    if(result.isStatus() == true){
                        System.out.println("[Upload Add Route]Add Route Success.");
                    }else{
                        System.out.println("[Upload Add Route]Add Route Fail.");
                        System.out.println("[Upload Add Route]Reason == " + result.getMessage());
                    }



                }

                //close
                inputStream.close();
                bufferedReader.close();

            } catch (FileNotFoundException e) {
                e.printStackTrace();
                return "Upload fail," + e.getMessage();
            } catch (IOException e) {
                e.printStackTrace();
                return "Upload Fail," + e.getMessage();
            }
            return "Upload Success.";
        } else {
            return "Upload Fail. Because the file is empty.";
        }
    }

}
