FROM openjdk:8-jdk


ADD ./target/ts-station-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-station-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-station-service-1.0.jar"]

EXPOSE 12345