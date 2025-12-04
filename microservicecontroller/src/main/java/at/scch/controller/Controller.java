package at.scch.controller;

import at.scch.dto.EvoArgs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static org.springframework.http.ResponseEntity.notFound;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequestMapping("/api/control")
public class Controller {

    private static final Logger LOGGER = LoggerFactory.getLogger(Controller.class);
    private static final String EVO_MASTER_LOG = "evomaster-log";
    private static final String MONGO_DUMPS_ROOT = "./dumps";
    private static Process microserviceApplication;
    private static Process evomasterApplication;


    @GetMapping(path = "/startWithEvoDriver")
    public HttpEntity<?> startWithEvoDriver() throws IOException {
        String message;
        if (microserviceApplication == null || !microserviceApplication.isAlive()) {
            message = String.format("Starting jar %s with EvoMaster controller %s", System.getenv("SERVICE_JAR"), System.getenv("EVO_MASTER_CONTROLLER"));
            LOGGER.info(message);
            ProcessBuilder pb = new ProcessBuilder("/bin/bash", "-c",
                    "java -Xmx200m -Xverify:none -cp ${SERVICE_JAR}-1.0.jar:evomaster-client-java-controller-2.0.0.jar:javax.servlet-api-4.0.1.jar -D'loader.main=${EVO_MASTER_CONTROLLER}' org.springframework.boot.loader.PropertiesLauncher")
                    .inheritIO();
            Map<String, String> env = pb.environment();
            env.put("JAVA_TOOL_OPTIONS", "-javaagent:/otel/otel/opentelemetry-javaagent.jar");
            microserviceApplication = pb.start();
        } else {
            message = String.format("Application of jar %s is already running", System.getenv("SERVICE_JAR"));
            LOGGER.info(message);
        }
        return ok(message);
    }

    @GetMapping(path = "/startNormal")
    public HttpEntity<?> startNormal() throws IOException {
        String message;
        if (microserviceApplication == null || !microserviceApplication.isAlive()) {
            message = String.format("Starting main Spring application of jar %s", System.getenv("SERVICE_JAR"));
            LOGGER.info(message);
            ProcessBuilder pb = new ProcessBuilder("/bin/bash", "-c",
                    "java -Xmx200m -Xverify:none -jar ${SERVICE_JAR}-1.0.jar --logging.file.name=app.logs --logging.file=app.logs")
                    .inheritIO();
            Map<String, String> env = pb.environment();
            env.put("JAVA_TOOL_OPTIONS", "-javaagent:/otel/otel/opentelemetry-javaagent.jar");
            microserviceApplication = pb.start();
        } else {
            message = String.format("Application of jar %s is already running", System.getenv("SERVICE_JAR"));
            LOGGER.info(message);
        }
        return ok(message);
    }


    @PostMapping(path = "/startGenerating")
    /**
     * !!!!!!!!!!!!!!!!!!!!!  CAUTION WARNING ATTENTION !!!!!!!!!!!!!!!!!!!!!!!!
     * ONLY USE THIS FOR RESEARCH PURPOSE / IN TRUSTED ENVIRONMENTS
     * WE PASS USER INPUT DIRECTLY TO THE COMMANDLINE -> ARBITRARY CODE EXECUTION
     */
    public HttpEntity<?> startGenerating(@RequestBody EvoArgs args) throws IOException {
        String message;
        if (evomasterApplication == null || !evomasterApplication.isAlive()) {
            message = String.format("Starting EvoMaster to generate tests with arguments: %s", args);
            LOGGER.info(message);
            ProcessBuilder pb = new ProcessBuilder("/bin/bash", "-c",
                    "java -jar evomaster.jar " + args);
            File log = new File(EVO_MASTER_LOG);
            pb.redirectErrorStream(true);
            pb.redirectOutput(log);
            evomasterApplication = pb.start();
        } else {
            message = "EvoMaster is already running";
            LOGGER.info(message);
        }
        return ok(message);
    }

    @GetMapping(path = "/evoMasterLogs")
    public HttpEntity<?> evoMasterLogs() {
        String log;
        try {
            log = String.join("\n", Files.readAllLines(Paths.get(EVO_MASTER_LOG)));
        } catch (IOException e) {
            return notFound().build();
        }
        if (evomasterApplication == null || !evomasterApplication.isAlive()) {
            return ok(log);
        } else {
            return ResponseEntity.status(HttpStatus.PARTIAL_CONTENT).body(log);
        }
    }

    @GetMapping(value = "/stop")
    public HttpEntity<?> stop() {
        String message;
        if (microserviceApplication != null && microserviceApplication.isAlive()) {
            message = String.format("Stopping jar %s ", System.getenv("SERVICE_JAR"));
            LOGGER.info(message);
            microserviceApplication.destroy();
        } else {
            message = String.format("Jar %s is not running", System.getenv("SERVICE_JAR"));
            LOGGER.info(message);
        }

        return ok(message);

    }

    @GetMapping(value = "/resetMongoDBs")
    public HttpEntity<?> resetMongoDBs() {
        String message;
        message = String.format("Resetting MongoDBs");
        LOGGER.info(message);
        try (Stream<Path> stream = Files.list(Paths.get("/app/dumps/"))) {
            List<Process> processes = stream
                    .filter(Files::isDirectory)
                    .map(Path::getFileName)
                    .map(Path::toString)
                    .map(mongoDB -> {
                        ProcessBuilder pb = new ProcessBuilder("/bin/bash", "-c",
                                "cd /app;./mongorestore --drop mongodb://" + mongoDB + " " + MONGO_DUMPS_ROOT +"/" +mongoDB +"/");
                        try {
                            return pb.start();
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    }).collect(Collectors.toList());
            for (Process process : processes) {
                process.waitFor();
            }
        } catch (IOException | InterruptedException e) {
            LOGGER.error(String.valueOf(e));
            return ResponseEntity.status(500).body(String.valueOf(e));
        }

        return ok(message);

    }
}
