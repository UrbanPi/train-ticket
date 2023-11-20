package contacts.init;

import contacts.service.ContactsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class InitData implements CommandLineRunner{

    @Autowired
    ContactsService service;

    @Override
    public void run(String... args)throws Exception{


    }
}
