package rebook;

import org.evomaster.client.java.controller.EmbeddedSutController;
import org.evomaster.client.java.controller.InstrumentedSutStarter;
import org.evomaster.client.java.controller.api.dto.AuthenticationDto;
import org.evomaster.client.java.controller.api.dto.CookieLoginDto;
import org.evomaster.client.java.controller.api.dto.SutInfoDto;
import org.evomaster.client.java.controller.internal.db.DbSpecification;
import org.evomaster.client.java.controller.problem.ProblemInfo;
import org.evomaster.client.java.controller.problem.RestProblem;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ConfigurableApplicationContext;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;


public class EmbeddedEvoMasterController extends EmbeddedSutController {
    private static final String MONGO_DUMPS_ROOT = "./dumps";
    private ConfigurableApplicationContext ctx;

    public static void main(String[] args) {

        int port = 40100;
        if (args.length > 0) {
            port = Integer.parseInt(args[0]);
        }

        EmbeddedEvoMasterController controller = new EmbeddedEvoMasterController(port);
        InstrumentedSutStarter starter = new InstrumentedSutStarter(controller);

        starter.start();
    }

    public EmbeddedEvoMasterController() {
        this(40100);
    }

    public EmbeddedEvoMasterController(int port) {
        setControllerPort(port);

    }

    @Override
    public String startSut() {
        ctx = SpringApplication.run(RebookApplication.class, new String[]{
                "--logging.file.name=app.logs", "--logging.file=app.logs"
        });
        resetStateOfSUT();
        return "http://localhost:" + getSutPort();
    }

    protected int getSutPort() {
        return (Integer) ((Map) ctx.getEnvironment()
                .getPropertySources().get("server.ports").getSource())
                .get("local.server.port");
    }


    @Override
    public boolean isSutRunning() {
        return ctx != null && ctx.isRunning();
    }

    @Override
    public void stopSut() {
        ctx.stop();
    }

    @Override
    public String getPackagePrefixesToCover() {
        return "rebook.";
    }

    @Override
    public void resetStateOfSUT() {
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
            throw new RuntimeException(e);
        }
    }

    @Override
    public ProblemInfo getProblemInfo() {
        return new RestProblem(
                "http://localhost:" + getSutPort() + "/v2/api-docs", null);
    }

    @Override
    public SutInfoDto.OutputFormat getPreferredOutputFormat() {
        return SutInfoDto.OutputFormat.JAVA_JUNIT_4;
    }

    @Override
    public List<AuthenticationDto> getInfoForAuthentication() {
        AuthenticationDto basicUserAuth = new AuthenticationDto("basicUser");
        CookieLoginDto cookieLoginDto = new CookieLoginDto();
        cookieLoginDto.contentType = CookieLoginDto.ContentType.JSON;
        cookieLoginDto.httpVerb = CookieLoginDto.HttpVerb.POST;
        cookieLoginDto.loginEndpointUrl = "http://ts-login-service:12342/login";
        cookieLoginDto.usernameField = "email";
        cookieLoginDto.username = "fdse_microservices@163.com";
        cookieLoginDto.passwordField = "password";
        cookieLoginDto.password = "DefaultPassword";
        basicUserAuth.cookieLogin = cookieLoginDto;

        return Arrays.asList(
                basicUserAuth
        );
    }

    @Override
    public List<DbSpecification> getDbSpecifications() {
        return null;
    }
}
