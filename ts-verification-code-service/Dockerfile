FROM openjdk:8-jdk


ADD ./target/ts-verification-code-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-verification-code-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-verification-code-service-1.0.jar"]

EXPOSE 15678