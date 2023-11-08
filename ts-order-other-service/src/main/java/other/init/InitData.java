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
        Order orderThree = new Order();
        orderThree.setId(UUID.fromString("d3c91694-d5b8-424c-9974-e14c89226e49"));
        orderThree.setBoughtDate(new Date());
        orderThree.setTravelDate(new Date("Sat Feb 24 00:00:00 GMT+0800 2017"));
        orderThree.setTravelTime(new Date("Mon May 04 09:00:00 GMT+0800 2013"));
        orderThree.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        orderThree.setContactsName("Contacts_One");
        orderThree.setDocumentType(1);
        orderThree.setContactsDocumentNumber("DocumentNumber_One");
        orderThree.setTrainNumber("Z1235");
        orderThree.setCoachNumber(5);
        orderThree.setSeatClass(2);
        orderThree.setSeatNumber("1");
        orderThree.setFrom("shanghai");
        orderThree.setTo("nanjing");
        orderThree.setStatus(0);
        orderThree.setPrice("100.0");
        service.initOrder(orderThree);
    }

}
