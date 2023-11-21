FROM openjdk:8-jdk


ADD ./target/ts-price-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-price-service-1.0.jar"]

EXPOSE 16579