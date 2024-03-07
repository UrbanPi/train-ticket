FROM openjdk:8-jdk


ADD ./target/ts-travel-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-travel-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-travel-service-1.0.jar"]

EXPOSE 12346