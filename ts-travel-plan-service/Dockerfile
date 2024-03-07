FROM openjdk:8-jdk


ADD ./target/ts-travel-plan-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-travel-plan-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-travel-plan-service-1.0.jar"]

EXPOSE 14322