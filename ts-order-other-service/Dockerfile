FROM openjdk:8-jdk

ADD ./target/ts-order-other-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-order-other-service-1.0.jar"]

EXPOSE 12032