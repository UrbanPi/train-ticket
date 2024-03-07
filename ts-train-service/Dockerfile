FROM openjdk:8-jdk


ADD ./target/ts-train-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-train-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-train-service-1.0.jar"]

EXPOSE 14567