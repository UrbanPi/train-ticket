package ticketinfo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import springfox.documentation.swagger2.annotations.EnableSwagger2;
import org.springframework.boot.web.client.RestTemplateBuilder;
//import org.springframework.cloud.sleuth.Span;
//import org.springframework.cloud.sleuth.SpanAdjuster;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.integration.annotation.IntegrationComponentScan;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.client.RestTemplate;
import ticketinfo.async.AsyncTask;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
@SpringBootApplication
@EnableSwagger2
@EnableAspectJAutoProxy(proxyTargetClass = true)
@EnableAsync
@IntegrationComponentScan
public class TicketInfoApplication {

    public static void main(String[] args) {
        SpringApplication.run(TicketInfoApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder.build();
    }

//    @Bean
//    public SpanAdjuster spanCollector() {
//        return new SpanAdjuster() {
//            @Override
//            public Span adjust(Span span) {
//                return span.toBuilder()
//                        .tag("controller_state",
//                                "Thread Pool :" + AsyncTask.size)
//                        //.name(span.getName() + "--------------------")
//                        .build();
//            }
//        };
//    }

}
