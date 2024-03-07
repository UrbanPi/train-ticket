FROM openjdk:8-jdk


ADD ./target/ts-price-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-price-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-price-service-1.0.jar"]

EXPOSE 16579