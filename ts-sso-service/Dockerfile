FROM openjdk:8-jdk


ADD ./target/ts-sso-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-sso-service-1.0.jar"]

EXPOSE 12349