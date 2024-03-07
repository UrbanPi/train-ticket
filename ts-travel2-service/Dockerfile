FROM openjdk:8-jdk


ADD ./target/ts-travel2-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-travel2-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-travel2-service-1.0.jar"]

EXPOSE 16346