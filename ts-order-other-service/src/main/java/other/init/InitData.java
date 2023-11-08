package other.init;

import other.domain.Order;
import other.service.OrderOtherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.UUID;

@Component
public class InitData implements CommandLineRunner {
    @Autowired
    OrderOtherService service;

    public void run(String... args)throws Exception{
        Order order = new Order();
        order.setId(UUID.fromString("5ad7750b-a68b-44c0-a9c0-32776b027703"));
        order.setBoughtDate(new Date());
        order.setTravelDate(new Date("Sat Jul 29 00:00:00 GMT+0800 2018"));
        order.setTravelTime(new Date("Mon May 04 09:02:00 GMT+0800 2013"));
        order.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        order.setContactsName("Contacts_One");
        order.setDocumentType(1);
        order.setContactsDocumentNumber("DocumentNumber_One");
        order.setTrainNumber("Z1234");
        order.setCoachNumber(5);
        order.setSeatClass(2);
        order.setSeatNumber("30");
        order.setFrom("shanghai");
        order.setTo("nanjing");
        order.setStatus(1);
        order.setPrice("100.0");
        service.initOrder(order);


        order.setId(UUID.fromString("5ad7750b-a68b-44c0-a9c0-32776b127703"));
        order.setBoughtDate(new Date());
        order.setTravelDate(new Date("Sat Jul 29 00:00:00 GMT+0800 2018"));
        order.setTravelTime(new Date("Mon May 04 09:02:00 GMT+0800 2013"));
        order.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        order.setContactsName("Contacts_One");
        order.setDocumentType(1);
        order.setContactsDocumentNumber("DocumentNumber_One");
        order.setTrainNumber("Z1234");
        order.setCoachNumber(5);
        order.setSeatClass(2);
        order.setSeatNumber("30");
        order.setFrom("shanghai");
        order.setTo("nanjing");
        order.setStatus(1);
        order.setPrice("100.0");
        service.initOrder(order);


    }

}
