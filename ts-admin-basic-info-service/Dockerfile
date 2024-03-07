FROM openjdk:8-jdk


ADD ./target/ts-admin-basic-info-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-admin-basic-info-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-admin-basic-info-service-1.0.jar"]

EXPOSE 18767