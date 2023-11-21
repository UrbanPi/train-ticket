package other;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import springfox.documentation.swagger2.annotations.EnableSwagger2;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.integration.annotation.IntegrationComponentScan;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.client.RestTemplate;
import other.service.OrderOtherServiceImpl;

@SpringBootApplication
@EnableSwagger2
@EnableAspectJAutoProxy(proxyTargetClass = true)
@EnableAsync
@IntegrationComponentScan
public class OrderOtherApplication {

    @Autowired
    OrderOtherServiceImpl orderOtherServiceImpl;

    public static void main(String[] args) throws Exception {
        SpringApplication.run(OrderOtherApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder.build();
    }

    //Two Kind Of Status
    //First： order-other-service async-task thread-pool：
    //                                       int a = AsyncTask.count
    //Second： station id on admin operating:
    //                                       String a = orderOtherServiceImpl.fromId;
    //                                       String b = orderOtherServiceImpl.toId;
    //Use the following method to print the key in Zipkin
/**
    @Bean
    public SpanAdjuster spanCollector() {
        return new SpanAdjuster() {
            @Override
            public Span adjust(Span span) {
                return span.toBuilder()
                        .tag("controller_state",
                                "<------------Your Key Here----------->")
                        //.name(span.getName() + "--------------------")
                        .build();
            }
        };
    }
 **/
}
