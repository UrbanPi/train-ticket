FROM openjdk:8-jdk

ADD ./target/ts-payment-service-1.0.jar /app/
CMD ["java", "-Xmx100m", "-jar", "/app/ts-payment-service-1.0.jar"]

EXPOSE 19001