FROM openjdk:8-jdk


ADD ./target/ts-route-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-route-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-route-service-1.0.jar"]

EXPOSE 11178