FROM openjdk:8-jdk
MAINTAINER Chenjie Xu <saberlilydian@163.com>

ADD ./target/ts-payment-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-payment-service-1.0.jar"]

EXPOSE 19001