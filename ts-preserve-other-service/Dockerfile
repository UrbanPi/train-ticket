FROM openjdk:8-jdk

ADD ./target/ts-preserve-other-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-preserve-other-service-1.0.jar"]

EXPOSE 14569