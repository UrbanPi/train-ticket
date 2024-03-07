FROM openjdk:8-jdk


ADD ./target/ts-route-plan-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-route-plan-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-route-plan-service-1.0.jar"]

EXPOSE 14578