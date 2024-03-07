FROM openjdk:8-jdk


ADD ./target/ts-notification-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-notification-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-notification-service-1.0.jar"]

EXPOSE 17853