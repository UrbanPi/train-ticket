FROM openjdk:8-jdk

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD ./target/ts-consign-price-service-1.0.jar /app/
ENV SW_AGENT_NAME=ts-consign-price-service
#CMD ["java", "-Xmx200m", "-javaagent:/skywalking/agent/skywalking-agent.jar", "-jar", "/app/ts-consign-price-service-1.0.jar"]
CMD java $JAVA_OPTIONS -javaagent:/skywalking/agent/skywalking-agent.jar -jar /app/ts-consign-price-service-1.0.jar

EXPOSE 16110