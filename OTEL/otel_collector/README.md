# Collector service for the OpenTelemetry extension in [otel_agent](../otel_agent/README.md)
Otel agents can push their traces to this simple service on the specified port. 
The service writes the incoming traces to a file in the directory of the executable jar.
In order to keep the size of the trace file small the service can be configured to only save traces confirming a given regular expression.

Arguments:

-t <file> : Name of the file for storing/appending traces.

-m <PUSH | PULL> : PUSH: the agents push their traces to this service. PULL: this service has to PULL traces from the agents.

-p <PORT_NUMBER> : Port to listen to.

-f <REG_EX> : (Optional) Regular expression for filtering incoming traces. This service only writes traces matching this regex to the output file.


Example command:

``java -jar TraceCollector-1.0.jar -t traces.txt -m PUSH -p 4242 -f "\"http.status_code\":2"``