FROM openjdk:8-jdk


ADD ./target/ts-execute-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-execute-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-execute-service-1.0.jar"]

EXPOSE 12386