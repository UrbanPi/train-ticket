FROM openjdk:8-jdk
MAINTAINER Chenjie Xu <15212010021@fudan.edu.cn>

ADD ./target/ts-train-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-train-service-1.0.jar"]

EXPOSE 14567