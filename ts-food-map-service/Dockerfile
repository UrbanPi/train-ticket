FROM openjdk:8-jdk


ADD ./target/ts-food-map-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-food-map-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-food-map-service-1.0.jar"]

EXPOSE 18855