FROM openjdk:8-jre
LABEL authors="Stefan Fischer, Pirmin Urbanke"

WORKDIR /otel

COPY TraceCollector-1.0.jar  /otel/

CMD ["java",  "-jar", "/otel/TraceCollector-1.0.jar", "-t", "traces.txt", "-m" , "PUSH", "-p", "4242", "-f", "\"http.status_code\":2"]

EXPOSE 4242
