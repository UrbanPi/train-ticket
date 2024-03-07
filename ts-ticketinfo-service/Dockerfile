FROM openjdk:8-jdk


ADD ./target/ts-ticketinfo-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-ticketinfo-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-ticketinfo-service-1.0.jar"]

EXPOSE 15681