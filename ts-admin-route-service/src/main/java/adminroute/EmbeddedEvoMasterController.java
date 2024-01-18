package adminroute;

import org.evomaster.client.java.controller.EmbeddedSutController;
import org.evomaster.client.java.controller.InstrumentedSutStarter;
import org.evomaster.client.java.controller.api.dto.AuthenticationDto;
import org.evomaster.client.java.controller.api.dto.SutInfoDto;
import org.evomaster.client.java.controller.api.dto.database.schema.DatabaseType;
import org.evomaster.client.java.controller.db.DbCleaner;
import org.evomaster.client.java.controller.internal.db.DbSpecification;
import org.evomaster.client.java.controller.problem.ProblemInfo;
import org.evomaster.client.java.controller.problem.RestProblem;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.jdbc.core.JdbcTemplate;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.Connection;
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

    public EmbeddedEvoMasterController() {
        this(40100);
    }

    public EmbeddedEvoMasterController(int port) {
        setControllerPort(port);

    }

    @Override
    public String startSut() {
        String sqlScript;
        try {
            sqlScript = String.join("\n", Files.readAllLines(Paths.get(INIT_DB_SCRIPT_PATH)));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        if (sqlScript.isEmpty()) {
            throw new RuntimeException("SQL script is empty");
        }

        ctx = SpringApplication.run(AdminRouteApplication.class, new String[]{
                "--logging.file.name=app.logs"
        });

        if (sqlConnection != null) {
            try {
                sqlConnection.close();
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }
        JdbcTemplate jdbc = ctx.getBean(JdbcTemplate.class);

        try {
            sqlConnection = jdbc.getDataSource().getConnection();
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
        return "adminroute.";
    }

    @Override
    public void resetStateOfSUT() {
        DbCleaner.clearDatabase(sqlConnection, schemaName, null, DatabaseType.MYSQL);
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
        return null;
    }


    @Override
    public List<DbSpecification> getDbSpecifications() {
        return dbSpecification;
    }
}
