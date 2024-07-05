from glob import glob
import os
import re
import subprocess
import shutil
import itertools
import pandas as pd
from pathlib import Path

from execute_evo_master.service_availability import filter_services
base = "./test_suites/"

def unpack_dump_archives(branch):
    branch = branch.rstrip('-reset')
    os.makedirs(f"../ExecutableTestSuites/dumps/{branch}", exist_ok=True)
    shutil.unpack_archive(f"./dump_archives_enhanced/dumps-enhanced-{branch}.tar.gz",
                          extract_dir=f"../ExecutableTestSuites/dumps/{branch}", format="gztar")

# TODO WARNING: Be aware of the correct python interpreter to call!
# TODO WARNING: On Windows and Linux there can be a difference between calling python and python3, which may not produce an error.
update_mongo_dumps = """private static void update_dumps() {{
        ProcessBuilder pb = new ProcessBuilder("python3", "./set_init_data.py",
                "--version", "{version}", "--service", "{service}");
        try {{
            Process p = pb.start();
            p.waitFor();
        }} catch (IOException | InterruptedException e) {{
            throw new RuntimeException(e);
        }}
    }}"""

"""
1.  Read
2. Adapt
2.1 variable names
2.2 endpoint URLS
2.3 Setup / Teardown / Stop
3. Distribute



Execution in Docker
+ No adaptations to endpoints needed


- Files are in Docker
- Container needed


Execution in local IDE
+ Tests visible / editable in IDE


- No actions from EvoMaster driver available
- Adaptations of endpoints needed
- Reset of MongoDBs needed


"""

before_class = """        controller.setupForGeneratedTest();
        baseUrlOfSut = controller.startSut();
        controller.registerOrExecuteInitSqlCommandsIfNeeded();
        assertNotNull(baseUrlOfSut);"""
before_target = """    @Before
    public void initTest() {
        controller.resetStateOfSUT();
    }"""

before_replace = """    @Before
    public void initTest() throws IOException {
        assertEquals("Resetting MongoDBs", resetStateOfSUT());
    }
    
    private String resetStateOfSUT() throws IOException {
        URL url = new URL("TARGET_URL");
        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        url.openStream()));
        StringBuilder response = new StringBuilder();
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
        return response.toString();
    }"""

after_class = """    @AfterClass
    public static void tearDown() {
        controller.stopSut();
    }"""



java_imports = """import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import org.junit.*;
import io.restassured.response.Response;
import org.hamcrest.Matchers;
"""

jpeg_replacement = """
        Response response = given().accept("*/*")
\g<1>\g<2>                .get(baseUrlOfSut + "/verification/generate\g<3>");
        response.then()
                .statusCode(200);
        byte[] actualBodyMagicBytesRange = Arrays.copyOfRange(response.body().asByteArray(), 0, 12);
        byte[] expectedMagicBytesJPEG_JFIF = new byte[]{
                (byte) 0xFF,
                (byte) 0xD8,
                (byte) 0xFF,
                (byte) 0xE0,
                (byte) 0x00,
                (byte) 0x10,
                (byte) 0x4A,
                (byte) 0x46,
                (byte) 0x49,
                (byte) 0x46,
                (byte) 0x00,
                (byte) 0x01
        };
        Assert.assertArrayEquals(expectedMagicBytesJPEG_JFIF, actualBodyMagicBytesRange);
"""

jpeg_regex = re.compile(r""" *given\(\)\.accept\("\*/\*"\)\n( *\.header\("x-EMextraHeader123", "[a-zA-Z0-9_]*"\)\n)?( *\.cookies\(cookies_fdse_microservices163com\)\n)? *\.get\(baseUrlOfSut \+ "/verification/generate(\?EMextraParam123=[a-zA-Z0-9_]+)?"\)\n *\.then\(\)\n *\.statusCode\(200\)\n *\.assertThat\(\)\n *\.body\((containsString\(\"����\u0000\u0010JFIF\u0000\u0001).*(\"\)\);?)""")



"""
coachNumber|contactsDocumentNumber|contactsName|documentType|from|price|seatClass|status|seatNumber|to|trainNumber|travelDate|travelTime
"""


dynamic_bought_date = re.compile(r"""
    (\s*\.body\(\s*"\s\{\s"\s\+\s*
    (:?"\s\\?"(loginid)\\?"[^\n]+\s*
        "\s\\?"(order)\\?"\s\{\s\+\s*)?
    (:?"\s\\?"(loginid|order|coachNumber|contactsDocumentNumber|accountId|contactsName|documentType|from|price|seatClass|status|seatNumber|to|trainNumber|travelDate|travelTime)\\?"[^\n]+\s*)*
    (:?"\s\}\s*"\s*\+\s*)?
    "\s\}\s*"\s*\)\s*\.
    post\(\s*baseUrlOfSut\s*\+\s*"[^\n]+\s*\.
    then\(\s*\)\s*\.
    statusCode\(\s*200\s*\)\s*\.
    assertThat\(\s*\)\s*\.
    contentType\(\s*"application/json"\s*\)\s*\.
    body\(\s*"'\s*status\s*'"\s*[^\n]+\s*\.
    body\(\s*"'\s*message\s*'"\s*[^\n]+\s*\.
    body\(\s*"'\s*order\s*'\s*\.\s*'boughtDate\s*'"\s*,\s*)(numberMatches\(\s*\d+\.\d+(:?E\d+)?\s*\))\s*\)
""", re.VERBOSE)

bought_date_in_list = re.compile(r"""
    (\.body\("'orders'\[\d+]\.'boughtDate'",\s*)numberMatches\((\d+\.\d+(:?E\d+)?)\)\)
    """, re.VERBOSE)


"""
Expected: (a value greater than <1708513643977L> and a value less than <1708513646977L>)
  Actual: 1708517162200
1708513643977
1708517162200
1708517646977
"""



def distribute_for_version(version: str):
    sut_controller = re.compile(r" +private static final SutHandler controller = .*\n")
    illegal_unicode_escape = re.compile(r"([^\\])(\\{3,})([^\\\"])")
    # uuid_message = re.compile(r"(containsString\([^\n]*?UUID has to be represented by standard 36-char representation)\\n.*(\"\)\);?)$", re.MULTILINE)
    # date_message = re.compile(r"(containsString\([^\n]*?'yyyy-MM-dd'T'HH:mm:ss.SSSZ', parsing fails \(leniency\? null\)\)).*(\"\)\);?)$", re.MULTILINE)
    deserialization = re.compile(r"(containsString\(\"Could not read JSON document: Can not deserialize value of type [^\n]*?)\\n at \[Source:.*(\"\)\);?)$", re.MULTILINE)
    construction = re.compile(r"(containsString\(\"Could not read JSON document: Can not construct instance of [^\n]*?)\\n at \[Source:.*(\"\)\);?)$", re.MULTILINE)
    login_token = re.compile(r"(\.body\(\"'loginAccountList'\[0]\.'loginToken'\", )(containsString\(\"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\"\))")
    station_id = re.compile(r"(\.body\()containsString\(\"[0-9a-f]{24}\"\)")
    numbers_no_exp = re.compile(r"(\.body\(\"'order'\.'[a-zA-Z0-9_]+'\", )numberMatches\((\d*)\.0\)")
    numbers_exp = re.compile(r"numberMatches\((\d*\.\d*E\d+)\)")
    bought_date = re.compile(r"(\.body\(\"'order'\.'boughtDate'\", )(numberMatches\((\d*)\.(\d*)(E\d+)\))")
    service_endpoints, _ = filter_services(version.rstrip("-reset"))
    for service in os.listdir(f"{base}/{version}"):
        # if "ts-admin-order" not in service and "ts-order-other" not in service:
        #     continue
        for test in os.listdir(f"{base}/{version}/{service}/tests"):
            f = Path(f"{base}/{version}/{service}/tests/{test}")
            content = f.read_text(encoding="utf8")
            content = content.replace("cookies_fdse_microservices@163.com", "cookies_fdse_microservices163com")
            content = content.replace("cookies_vip_microservices@163.com", "cookies_vip_microservices163com")
            content = content.replace("ts-login-service:12342", "localhost:30075")
            # Set cookie required for login. The actual value is not important, it just has to be there
            content = content.replace(""".post("http://localhost:30075/login")
            .then().extract().cookies();""", """.cookie("YsbCaptcha=some-value")
            .post("http://localhost:30075/login")
            .then().extract().cookies();""")
            serv = [el for el in service_endpoints if el["name"] == service][0]
            # Set baseUrl of the SUT as local address. (Convention: the SUT port is the port number -600)
            content = content.replace("baseUrlOfSut;", f"baseUrlOfSut = \"http://localhost:{serv['port']-600}\";")
            content = sut_controller.sub("", content)
            content = illegal_unicode_escape.sub("\g<1>\\\\\\\\\\\\\\\\\g<3>", content)
            # Replace runtime specific parts of assertions:
            content = deserialization.sub(r"\g<1>\g<2>", content)
            content = construction.sub(r"\g<1>\g<2>", content)

            content = login_token.sub("\g<1>notNullValue(String.class)", content)
            content = station_id.sub("\g<1>notNullValue(String.class)", content)
            # content = bought_date.sub("\g<1>Matchers.allOf(greaterThan(System.currentTimeMillis()-1000L), lessThan(System.currentTimeMillis()))", content)
            if """.body("'order'.'boughtDate'",""" in content:
                content = dynamic_bought_date.sub("\g<1>Matchers.allOf(greaterThan(System.currentTimeMillis()-3000L), lessThan(System.currentTimeMillis())))", content)
            # In the current tests EvoMaster only asserts up to three elements of a returned list (can be configured)
            # These three elements are all initial data / data present at startup
            # Maybe due to timezone issues during generation of the database dumps the timestamps are off by one hour.
            # However, there may be more to this because EvoMaster probably would not generate wrong assertions if the
            # returned timestamps are always off by one hour.
            content = bought_date_in_list.sub("\g<1>Matchers.allOf(greaterThan(((long)\g<2>)-3000L), lessThan(((long)\g<2>)+361*1000L)))", content)
            content = jpeg_regex.sub(jpeg_replacement, content)

            # Setup and reset
            content = content.replace(before_target, before_replace.replace("TARGET_URL", f"http://localhost:{serv['port']}/api/control/resetMongoDBs"))
            content = content.replace(after_class, "")
            content = content.replace(before_class, "        update_dumps();")
            mongo_update = update_mongo_dumps.format(
                version=version.replace('-reset',''),
                service=service)
            content = content.replace("@BeforeClass", f"{mongo_update}\n\n    @BeforeClass")
            content = java_imports + content
            version_formatted = version.replace("-","_").lower()
            service_formatted = service.replace("-","_").lower()

            content = f"package {version_formatted}.{service_formatted};\n\n" + content
            target_path = f"./../ExecutableTestSuites/src/test/java/{version_formatted}/{service_formatted}"
            os.makedirs(target_path, exist_ok=True)
            Path(f"{target_path}/{test}").write_text(content, encoding="utf8")


if __name__ == '__main__':
    for branch in os.listdir(base):
        if branch.startswith("ts-error-") or branch.startswith("ts-error-cleaned"):
            # unpack_dump_archives(branch)
            distribute_for_version(branch)

