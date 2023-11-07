FROM openjdk:8-jdk

ADD ./target/ts-basic-service-1.0.jar /app/
CMD ["java", "-Xmx1200m", "-jar", "/app/ts-basic-service-1.0.jar"]

EXPOSE 15680