FROM openjdk:8-jdk


ADD ./target/ts-seat-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-seat-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-seat-service-1.0.jar"]

EXPOSE 18898