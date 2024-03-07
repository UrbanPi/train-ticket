FROM openjdk:8-jdk


ADD ./target/ts-order-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-order-service
CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-order-service-1.0.jar"]
#CMD java $JAVA_OPTIONS -jar /app/ts-order-service-1.0.jar

EXPOSE 12031