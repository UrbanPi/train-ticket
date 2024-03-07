FROM openjdk:8-jdk


ADD ./target/ts-admin-order-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-admin-order-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-admin-order-service-1.0.jar"]

EXPOSE 16112