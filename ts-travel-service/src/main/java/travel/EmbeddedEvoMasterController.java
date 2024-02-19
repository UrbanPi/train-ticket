package travel;

import org.evomaster.client.java.controller.EmbeddedSutController;
import org.evomaster.client.java.controller.InstrumentedSutStarter;
import org.evomaster.client.java.controller.api.dto.AuthenticationDto;
import org.evomaster.client.java.controller.api.dto.JsonTokenPostLoginDto;
import org.evomaster.client.java.controller.api.dto.SutInfoDto;
import org.evomaster.client.java.controller.api.dto.database.schema.DatabaseType;
import org.evomaster.client.java.controller.db.DbCleaner;
import org.evomaster.client.java.controller.db.SqlScriptRunner;
import org.evomaster.client.java.controller.internal.db.DbSpecification;
import org.evomaster.client.java.controller.problem.ProblemInfo;
import org.evomaster.client.java.controller.problem.RestProblem;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ConfigurableApplicationContext;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.*;

public class EmbeddedEvoMasterController extends EmbeddedSutController {
    public static void main(String[] args) {

        int port = 40100;
        if (args.length > 0) {
            port = Integer.parseInt(args[0]);
        }

        EmbeddedEvoMasterController controller = new EmbeddedEvoMasterController(port);
        InstrumentedSutStarter starter = new InstrumentedSutStarter(controller);

        starter.start();
    }
    private static final String schemaName = "ts";
    private ConfigurableApplicationContext ctx;
    private Connection sqlConnection;
    private String INIT_DB_SCRIPT_PATH = "./complete.sql";
    private List<DbSpecification> dbSpecification = new ArrayList<>();
    private String sqlScript;
    public EmbeddedEvoMasterController() {
        this(40100);
    }

    public EmbeddedEvoMasterController(int port) {
        setControllerPort(port);

    }

    @Override
    public String startSut() {
        try {
            sqlScript = String.join("\n", Files.readAllLines(Paths.get(INIT_DB_SCRIPT_PATH)));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        if (sqlScript.isEmpty()) {
            throw new RuntimeException("SQL script is empty");
        }

        ctx = SpringApplication.run(TravelApplication.class, new String[]{
                "--logging.file.name=app.logs"
        });

        if (sqlConnection != null) {
            try {
                sqlConnection.close();
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }

        try {
            sqlConnection = DriverManager.getConnection("jdbc:mysql://ts-db-mysql-leader:3306/ts?useSSL=false", "ts", "Ts_123456");
//            Alternative to hardcoded SQL connection, get connection from spring context (code below).
//            Beware, some services do not have a direct connection to the DB but still modify it through other services
//            (e.g. ts-admin-basic-info-service). These services still need to reset the DB somehow.
//            When deploying the application with individual databases a different approach is needed e.g. store all
//            DB connection info here and reset each individually.

//            JdbcTemplate jdbc = ctx.getBean(JdbcTemplate.class);
//            sqlConnection = jdbc.getDataSource().getConnection();

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        /*
            the application will be initialized some data in database
            to consistently manage data by evomaster
         */

        DbCleaner.clearDatabase(sqlConnection, schemaName, null, DatabaseType.MYSQL);

        dbSpecification = Arrays.asList(new DbSpecification(DatabaseType.MYSQL, sqlConnection)
                .withInitSqlScript(sqlScript)
                .withSchemas(schemaName));

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
        return "travel.";
    }

    @Override
    public void resetStateOfSUT() {
        DbCleaner.clearDatabase(sqlConnection, schemaName, null, DatabaseType.MYSQL);
        SqlScriptRunner.runScript(sqlConnection, new StringReader(sqlScript));
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
        String loginEndpoint = "http://ts-auth-service:12340/api/v1/users/login";
        String headerPrefix = "Bearer ";
        String jwtLocation = "/data/token"; // JSON Pointer

        AuthenticationDto basicUserAuth = new AuthenticationDto("basicUser");
        JsonTokenPostLoginDto basicUserInfo = new JsonTokenPostLoginDto();
        basicUserInfo.endpoint = loginEndpoint;
        basicUserInfo.userId = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f";
        basicUserInfo.jsonPayload = "{\"username\":\"fdse_microservice\",\"password\":\"111111\",\"verificationCode\":\"1234\"}";
        basicUserInfo.headerPrefix = headerPrefix;
        basicUserInfo.extractTokenField = jwtLocation;
        basicUserAuth.jsonTokenPostLogin = basicUserInfo;


        AuthenticationDto adminUserAuth = new AuthenticationDto("AdminUser");
        JsonTokenPostLoginDto adminUserInfo = new JsonTokenPostLoginDto();
        adminUserInfo.endpoint = loginEndpoint;
        adminUserInfo.userId = "randomUUID";
        adminUserInfo.jsonPayload = "{\"username\":\"admin\",\"password\":\"222222\"}";
        adminUserInfo.headerPrefix = headerPrefix;
        adminUserInfo.extractTokenField = jwtLocation;
        adminUserAuth.jsonTokenPostLogin = adminUserInfo;

        return Arrays.asList(
                basicUserAuth,
                adminUserAuth
        );
    }

    @Override
    public List<DbSpecification> getDbSpecifications() {
        return dbSpecification;
    }
}
