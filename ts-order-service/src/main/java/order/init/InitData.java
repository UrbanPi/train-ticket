package order.init;

import order.domain.Order;
import order.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.UUID;

/**
 * Created by Chenjie Xu on 2017/6/5.
 */
@Component
public class InitData implements CommandLineRunner {
    @Autowired
    OrderService service;

    public void run(String... args)throws Exception{

    }

}

