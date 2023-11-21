FROM openjdk:8-jdk


ADD ./target/ts-launcher-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-launcher-1.0.jar"]

EXPOSE 12898