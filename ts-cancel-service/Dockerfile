FROM openjdk:8-jdk

ADD ./target/ts-cancel-service-1.0.jar /app/
CMD ["java", "-Xmx100m", "-jar", "/app/ts-cancel-service-1.0.jar"]

EXPOSE 18885