FROM openjdk:8-jdk

ADD ./target/ts-preserve-service-1.0.jar /app/
CMD ["java", "-Xmx100m", "-jar", "/app/ts-preserve-service-1.0.jar"]

EXPOSE 14568