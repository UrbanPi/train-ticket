FROM openjdk:8-jdk

ADD ./target/ts-route-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-route-service-1.0.jar"]

EXPOSE 11178