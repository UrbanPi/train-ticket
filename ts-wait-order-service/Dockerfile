FROM openjdk:8-jdk



ADD ./target/ts-wait-order-service-1.0.jar /app/
CMD ["java", "-Xmx200m",  "-jar", "/app/ts-wait-order-service-1.0.jar"]

EXPOSE 15678