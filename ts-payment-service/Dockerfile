FROM openjdk:8-jdk


ADD ./target/ts-payment-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-payment-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-payment-service-1.0.jar"]

EXPOSE 19001