FROM openjdk:8-jdk


ADD ./target/ts-assurance-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-assurance-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-assurance-service-1.0.jar"]

EXPOSE 18888