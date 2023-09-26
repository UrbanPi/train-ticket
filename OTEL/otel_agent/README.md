
# OpenTelemetry Extension to record http requests and responses

We created an extension to OpenTelemetry Java Agent to add the payloads of HTTP requests and responses to the existing traces.


All extensions are made in `https://git.scch.at/projects/SMART/repos/engel-ai/browse/TestAgent?at=refs%2Fheads%2FRENE-experiments`


## Tracing the application

The `opentelemetry-javaagent.jar` is a build of the entire java agent already containing our extension (i.e. the extension JAR is not extra needed).
To use the extension we need to pass the option `otel.javaagent.extensions=opentelemetry-ext.at.scch.testAgent.jar`.

The `opentelemetry-ext.at.scch.testAgent.jar-1.0-all.jar` is the extension without the OTEL agent. This can also be used with existing OTEL Java agents by passing it with the option `otel.javaagent.extensions`.

VM arguments for JVM:

```
-javaagent:/path/to/opentelemetry-javaagent.jar 
-Dotel.traces.expoter=logging 
-Dotel.javaagent.extensions=opentelemetry-ext.at.scch.testAgent.jar 
-Dotel.javaagent.debug=false 
-Xverify:none
```

Additionally, the extension requires a configuration file, see: `scch-testAgent.properties`.
This file needs to be copied into the working directory, from where the application is running.


## Collecting traces

### Using OTEL Collector

OpenTelemetry offers a collector that collects all the traces from distributed agents in one location.
[https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

We could check if we can collect all the traces using this for executing TrainTicket.


### Our own solution

Can be done with code using `at.scch.opentelemetry.tracecollector.jar-1.0-all.jar`.

Example:

```java
import at.scch.rl.traceCollector.TraceCollector;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Main {

    public static void main(String[] args) throws InterruptedException {
        while(true){
            collectTraces("127.0.0.1:4242", new File("traces.txt"));
            Thread.sleep(1000);
        }
    }

    public static void collectTraces(String url, File target){
        try {
            FileWriter fw = new FileWriter(target, true);
            BufferedWriter bw = new BufferedWriter(fw);

            TraceCollector.collectTraces(url, rawSpan -> {
                if(rawSpan.contains("\"http.status_code\":200")) { // Filter only spans with http status code 200.
//                if(rawSpan.contains("\"kind\":\"SERVER\"")) {
                    try {
                        bw.write(rawSpan);
                        bw.newLine();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            });

            bw.flush();
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

The above code will get the spans (i.e., trace parts) that represent http requests with a http status code 200 and print them into a file.

Example file:

```
{"traceId":"1f6125454090d96cc3ecd038eedc69df","spanId":"eccef1a6e7d175e6","kind":"SERVER","name":"GET /api/fisher/{m}/{n}/{x}","start":1691740553193000000,"end":1691740555148935600,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/fisher/4/3/9","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-1","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/fisher/{m}/{n}/{x}","response.body":"{\"resultAsInt\":null,\"resultAsDouble\":0.9491251299320057}","net.protocol.name":"http","net.sock.peer.port":61400,"http.method":"GET","http.scheme":"http","thread.id":36,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
{"traceId":"62f2ef112026d67aa3deba25576569fa","spanId":"77ce4357ae3e6627","kind":"SERVER","name":"GET /api/expint/{n}/{x}","start":1691740554087000000,"end":1691740555148511600,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/expint/3/9","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-4","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/expint/{n}/{x}","response.body":"{\"resultAsInt\":null,\"resultAsDouble\":1.0478627815975423E-5}","net.protocol.name":"http","net.sock.peer.port":61402,"http.method":"GET","http.scheme":"http","thread.id":39,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
{"traceId":"8908b67be52d231be81d31cebba1d817","spanId":"309f83a7bd89b463","kind":"SERVER","name":"GET /api/bessj/{n}/{x}","start":1691740555979000000,"end":1691740555991417200,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/bessj/3/9","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-2","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/bessj/{n}/{x}","response.body":"{\"resultAsInt\":null,\"resultAsDouble\":-0.18093519040457304}","net.protocol.name":"http","net.sock.peer.port":61402,"http.method":"GET","http.scheme":"http","thread.id":37,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
{"traceId":"071813fb7ddd6a4b1d2e450398b01a54","spanId":"218a673643955f58","kind":"SERVER","name":"GET /api/gammq/{a}/{x}","start":1691740556862000000,"end":1691740556874441700,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/gammq/3/9","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-3","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/gammq/{a}/{x}","response.body":"{\"resultAsInt\":null,\"resultAsDouble\":0.00623219510637732}","net.protocol.name":"http","net.sock.peer.port":61402,"http.method":"GET","http.scheme":"http","thread.id":38,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
{"traceId":"9fc9762b6a443798638b1f3b77760d0d","spanId":"f6301c2f0c0b2f15","kind":"SERVER","name":"GET /api/remainder/{a}/{b}","start":1691740557686000000,"end":1691740557700976900,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/remainder/9/4","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-5","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/remainder/{a}/{b}","response.body":"{\"resultAsInt\":1,\"resultAsDouble\":null}","net.protocol.name":"http","net.sock.peer.port":61402,"http.method":"GET","http.scheme":"http","thread.id":40,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
{"traceId":"7e2c4c8add3013bb5fcbdd665f1c3339","spanId":"97fd35adc97737ed","kind":"SERVER","name":"GET /api/triangle/{a}/{b}/{c}","start":1691740558477000000,"end":1691740558489902400,"attributes":{"user_agent.original":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0","net.host.name":"localhost","request.CharacterEncoding":"UTF-8","http.target":"/api/triangle/10/10/13","net.sock.peer.addr":"127.0.0.1","response.ContentType":"application/json;charset=UTF-8","thread.name":"http-nio-8080-exec-6","http.status_code":200,"net.sock.host.addr":"127.0.0.1","response.BufferSize":8192,"net.host.port":8080,"http.route":"/api/triangle/{a}/{b}/{c}","response.body":"{\"resultAsInt\":2,\"resultAsDouble\":null}","net.protocol.name":"http","net.sock.peer.port":61402,"http.method":"GET","http.scheme":"http","thread.id":41,"net.protocol.version":"1.1"},"tracer":"io.opentelemetry.tomcat-7.0"}
```


#### Processing

To further process the spans you can use `TraceCollector.parseSpan(line);` to parse the lines again into the OpenTelemetry like datastructure.

Each Span has attributes that can be checked with their key (e.g., `request.body`, `response.body`).
Get them with `Span.getAttribute(String key)`.

