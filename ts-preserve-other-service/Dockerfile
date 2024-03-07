FROM openjdk:8-jdk


ADD ./target/ts-preserve-other-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-preserve-other-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-preserve-other-service-1.0.jar"]

EXPOSE 14569