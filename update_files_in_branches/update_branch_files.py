import pathlib
from glob import glob
import os
import re
import subprocess
import shutil
import tarfile
from pathlib import Path

from add_update_files_for_evomaster import add_embedded_evo_master_controller, add_spring_fox_config

branches = [
            # "master",
    "ts-error-F1",
    "ts-error-F2",
    "ts-error-F3",
    "ts-error-F4",
    "ts-error-F5",
    "ts-error-F6",
            "ts-error-F7",
    "ts-error-F8",
    "ts-error-F9", "ts-error-F10",
            "ts-error-F11", "ts-error-F12",
            "ts-error-F13", "ts-error-F14", "ts-error-F15", "ts-error-F16",
    "ts-error-F17", "ts-error-F18",
            "ts-error-F19", "ts-error-F20", "ts-error-F21", "ts-error-F22",
    "ts-error-cleaned"
            ]
file_mapping = {
    # "./../update_files_in_branches/files_to_update/build-and-push.yml": ".github/workflows/",
    # "./../update_files_in_branches/files_to_update/deploy-locally.yaml": ".github/workflows/",
    # "./../update_files_in_branches/files_to_update/deploy-to-cluster.yaml": ".github/workflows/",
    # "./../update_files_in_branches/files_to_update/reset-deployment.yaml": ".github/workflows/",
    # "./../update_files_in_branches/files_to_update/reset-deployment-locally.yaml": ".github/workflows/",
    # "./../update_files_in_branches/files_to_update/get_swagger_definitions.py": "swagger_definitions/",
    # "./../update_files_in_branches/files_to_update/publish-docker-images.sh": "script/",
    "./../update_files_in_branches/files_to_update/prometheus.yml": "deployment/kubernetes-manifests/prometheus/",
}


def enable_mongodb_query_logging():
    for file in filter(None,[f if "mongodb" in Path(f).read_text() and "target" not in f else None for f in glob("./**/application.yml", recursive=True)]):
        path = Path(file)
        text = f"{path.read_text(encoding='utf8')}\nlogging:\n  level:\n    org.springframework.data.mongodb.core.MongoTemplate: DEBUG"
        path.write_text(text, encoding="utf8")


def update_branches():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)

        # Make changes
        evo_dependency = """	<dependency>
			<groupId>org.evomaster</groupId>
			<artifactId>evomaster-client-java-controller</artifactId>
			<version>2.0.0</version>
	    </dependency>
	</dependencies>\n"""
        with open("./pom.xml", "r", encoding="utf8") as pomf:
            pom = pomf.read()
        pom = pom.replace("</dependencies>\n", evo_dependency)
        with open("./pom.xml", "w", encoding="utf8") as pomf:
            pomf.write(pom)
        # Commit -2
        subprocess.check_output(["git", "commit", "-a", "-m", "Add EvoMaster dependency"], shell=False)

        package_mappings = add_embedded_evo_master_controller()
        subprocess.check_output(["git", "add", "./**/EmbeddedEvoMasterController.java"], shell=False)
        # Commit -1
        subprocess.check_output(["git", "commit", "-a", "-m", "Add preliminary EvoMasterController"], shell=False)

        add_spring_fox_config()
        subprocess.check_output(["git", "add", "./**/SpringFoxConfig.java"], shell=False)
        # Commit 0
        subprocess.check_output(["git", "commit", "-a", "-m", "Add swagger configuration"], shell=False)


        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml", "r", encoding="utf8") as svcf:
            svc = svcf.read()
        t = re.sub(r"^ {6}nodePort: 303(\d\d)", r"\g<0>\n    - name: evomaster\n      port: 40100\n      nodePort: 305\g<1>\n    - name: mscontr\n      port: 9090\n      nodePort: 306\g<1>", svc, flags=re.MULTILINE)
        t = re.sub(r"^#.*$\n", "", t, flags=re.MULTILINE)  # Clear comments
        for r in ["30063", "30048"]:  # ts-news-service and ts-ticket-office-service
            t = t.replace(f"""{r}
        - name: metric
          port: 9464
          nodePort: {r}""", r)
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml", "w", encoding="utf8") as svcf:
            svcf.write(t)

        # with open("./../update_files_in_branches/files_to_update/otel_deploy.yaml", "r", encoding="utf8") as otel_deployf:
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "r", encoding="utf8") as otel_deployf:
            otel_deploy = otel_deployf.read()
        t = re.sub(r"^#.*$\n", "", otel_deploy, flags=re.MULTILINE)  # Clear comments
        replacement_empty_dirs = """\n          emptyDir: {}
        - name: javaxservlet-vol
          emptyDir: {}
        - name: evomaster-vol
          emptyDir: {}
        - name: persistenceinit-vol
          emptyDir: {}
        - name: microservicecontroller-vol
          emptyDir: {}"""
        t = t.replace("\n          emptyDir: {}", replacement_empty_dirs)

        replacement_init_containers = f"""\n          args: [ "-c", "cp -R /otel /agent/" ]
        - name: javaxservlet-container
          image: containers.github.scch.at/contest/trainticket/javaxservlet:latest
          imagePullPolicy: Always
          volumeMounts:
            - name: javaxservlet-vol
              mountPath: /javaxservlet-mnt
          command: [ "/bin/sh" ]
          args: [ "-c", "cp -R /javax /javaxservlet-mnt/" ]
        - name: evomaster-container
          image: containers.github.scch.at/contest/trainticket/evomaster:latest
          imagePullPolicy: Always
          volumeMounts:
            - name: evomaster-vol
              mountPath: /evomaster-mnt
          command: [ "/bin/sh" ]
          args: [ "-c", "cp -R /evomaster /evomaster-mnt/" ]
        - name: persistenceinit-container
          image: containers.github.scch.at/contest/trainticket/persinit:{branch}
          imagePullPolicy: Always
          volumeMounts:
            - name: persistenceinit-vol
              mountPath: /persinit-mnt
          command: [ "/bin/sh" ]
          args: [ "-c", "cp -R /persinit /persinit-mnt/" ]
        - name: microservicecontroller-container
          image: containers.github.scch.at/contest/trainticket/microservicecontroller:latest
          imagePullPolicy: Always
          volumeMounts:
            - name: microservicecontroller-vol
              mountPath: /microservicecontroller-mnt
          command: [ "/bin/sh" ]
          args: [ "-c", "cp -R /microservicecontroller /microservicecontroller-mnt/" ]"""
        t = t.replace('\n          args: [ "-c", "cp -R /otel /agent/" ]', replacement_init_containers)

        replacement_volume_mounts = """\n              mountPath: /otel
            - name: javaxservlet-vol
              mountPath: /javax
            - name: evomaster-vol
              mountPath: /evomaster
            - name: persistenceinit-vol
              mountPath: /persinit
            - name: microservicecontroller-vol
              mountPath: /microservicecontroller"""
        t = t.replace("\n              mountPath: /otel", replacement_volume_mounts)

        t = t.replace("""

            - name: SERVICE_JAR""", "\n            - name: SERVICE_JAR")
        for service, package in package_mappings.items():
            repl_serv_jar = f'''            - name: EVO_MASTER_CONTROLLER
              value: "{package}.EmbeddedEvoMasterController"
            - name: SERVICE_JAR
              value: "{service}"'''

            t = t.replace(f'''            - name: SERVICE_JAR
              value: "{service}"''', repl_serv_jar)

        repl_args = 'args: [ "-c", "cp /otel/otel/scch-testAgent.properties /app/; cp /javax/javax/javax.servlet-api-4.0.1.jar /app/; cp /evomaster/evomaster/evomaster-client-java-controller-2.0.0.jar /app/; cp /evomaster/evomaster/evomaster.jar /app/; cp -R /persinit/persinit/ /app/; cp /microservicecontroller/microservicecontroller/microservicecontroller-1.0.jar /app/; cd /app/; java -jar microservicecontroller-1.0.jar"]'
        t = t.replace('args: [ "-c", "cp /otel/otel/scch-testAgent.properties /app/; cp /otel/otel/javax.servlet-api-4.0.1.jar /app/; cd /app/; java -Xmx200m -Xverify:none -jar $(SERVICE_JAR)-1.0.jar --logging.file=./app.logs" ]', repl_args)
        t = t.replace('args: [ "-c", "cp /otel/otel/scch-testAgent.properties /app/; cp /otel/otel/javax.servlet-api-4.0.1.jar /app/; cd /app/; java -Xmx200m -Xverify:none -jar $(SERVICE_JAR)-1.0.jar --logging.file=./app.logs"]', repl_args)
        repl_container_ports = """            - name: metric
              containerPort: 9464
            - name: evomaster
              containerPort: 40100
            - name: mscontr
              containerPort: 9090"""

        t = re.sub(r"^ {12}- containerPort: \d{5}", r"\g<0>\n"+repl_container_ports, t, flags=re.MULTILINE)
        repl_readiness_probe = """              port: 9090"""
        t = re.sub(r"^ {14}port: \d{5}", repl_readiness_probe, t, flags=re.MULTILINE)

        # Revert ports for ts-news-service and ts-ticket-office-service
        revert = ["12862", "16108"]  # ts-news-service and ts-ticket-office-service
        for r in revert:
            rev1 = f"""            - containerPort: {r}
            - name: metric
              containerPort: 9464
            - name: evomaster
              containerPort: 40100
            - name: mscontr
              containerPort: 9090"""
            t = t.replace(rev1, f"            - containerPort: {r}")
            rev2 = f"""            - containerPort: {r}
          resources:
            requests:
              cpu: 100m
              memory: 250Mi
            limits:
              cpu: 500m
              memory: 500Mi
          readinessProbe:
            tcpSocket:
              port: 9090"""
            t = t.replace(rev2, f"""            - containerPort: {r}
          resources:
            requests:
              cpu: 100m
              memory: 250Mi
            limits:
              cpu: 500m
              memory: 500Mi
          readinessProbe:
            tcpSocket:
              port: {r}""")

        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "w", encoding="utf8") as otel_deployf:
            otel_deployf.write(t)

    #     # Commit 1
        subprocess.check_output(["git", "commit", "-a", "-m", "Adapt deployment to evomaster setup"], shell=False)

        with open("./deployment/kubernetes-manifests/prometheus/prometheus-configmap.yml", "r", encoding="utf8") as prometheus_f:
            prom: str = prometheus_f.read()
        # with open("./../update_files_in_branches/files_to_update/prometheus-configmap.yml", "r", encoding="utf8") as prometheus_f:
        #     prom: str = prometheus_f.read()

        prom = prom.replace("\n        scrape_interval: 30s", "")
        prom = prom.replace("      - /etc/config/rules/*.rules", "      - /etc/config/rules/*.rules\n    global:\n      scrape_interval: 15s")

        with open("./deployment/kubernetes-manifests/prometheus/prometheus-configmap.yml", "w", encoding="utf8") as prometheus_f:
            prometheus_f.write(prom)
        # Commit 2
        subprocess.check_output(["git", "commit", "-a", "-m", "Set global prometheus scrape interval"], shell=False)


        # for file in [f for f in glob.glob("./**/?nitData.java", recursive=True)]:
        #     path = Path(file)
        #     path = path.rename(Path(path.parent, "InitData.java"))
        #     text = path.read_text(encoding="utf8")
        #     text = text.replace("public class initData implements", "public class InitData implements")
            # path.write_text(text, encoding="utf8")
            # old_path = str(path)
            # new_path = str(Path(path.parent, "InitData.java"))
            # if old_path != new_path:
            #     subprocess.check_output(["git", "mv", old_path, new_path], shell=False)
            # subprocess.check_output(["git", "add", str(path)], shell=False)
        # p = Path("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml")
        # text = p.read_text(encoding="utf8")
        # text = text.replace("error-f", "ts-error-F")
        # p.write_text(text, encoding="utf8")

    # # Copy files
        for src, dst in file_mapping.items():
            shutil.copy(src, dst)
        # Commit 3
        subprocess.check_output(["git", "commit", "-a", "-m", "Add March remote desktop as runner"], shell=False)

    # # Copy files
        shutil.copy( "./../update_files_in_branches/files_to_update/deploy.sh", "hack/deploy/",)
        # Commit 4
        subprocess.check_output(["git", "commit", "-a", "-m", "Change order of deployments to avoid random port conflicts"], shell=False)

    # PersistenceInit
        shutil.copy("./../update_files_in_branches/files_to_update/.gitattributes", "./",)
        subprocess.check_output(["git", "add", "./.gitattributes"], shell=False)
        os.makedirs("./PersistenceInit", exist_ok=True)
        persinit = {
            "./../update_files_in_branches/files_to_update/Dockerfile": "./PersistenceInit/Dockerfile",
            # "./../update_files_in_branches/files_to_update/publish-persinit-image.sh": "./PersistenceInit/publish-persinit-image.sh",
            "./../update_files_in_branches/files_to_update/dumps.tar.gz": "./PersistenceInit/dumps.tar.gz",
        }
        for src, dst in persinit.items():
            shutil.copy(src, dst)
            subprocess.check_output(["git", "add", dst], shell=False)

        with open("./../update_files_in_branches/files_to_update/publish-persinit-image.sh", "r", encoding="utf8") as pers_f:
            pers = pers_f.read()
        pers = pers.replace("VERSION_XXXXX", branch)
        with open("./PersistenceInit/publish-persinit-image.sh", "w", encoding="utf8") as pers_f:
            pers_f.write(pers)
        subprocess.check_output(["git", "add", "./PersistenceInit/publish-persinit-image.sh"], shell=False)

        # Commit 5
        subprocess.check_output(["git", "commit", "-a", "-m", "Add preliminary PersistenceInit data"], shell=False)


        #  Add exec bit
        # Add files
        # subprocess.check_output(["git", "add", ".github/workflows"], shell=False)
        # if len(subprocess.check_output(["git", "status", "-s"], shell=False)) != 0:
        #     # Commit files, when there are changes
        #     subprocess.check_output(["git", "commit", "-a", "-m", message], shell=False)
        # subprocess.check_output(["git", "push", "-a", "-m", message], shell=False) # We can push everything later
        # Execute: git push --all

def remove_java_tool_options():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "r", encoding="utf8") as otel_deployf:
            otel_deploy = otel_deployf.read()
        otel_deploy = otel_deploy.replace('\n  JAVA_TOOL_OPTIONS: "-javaagent:/otel/otel/opentelemetry-javaagent.jar"', "")
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "w", encoding="utf8") as otel_deployf:
            otel_deployf.write(otel_deploy)
        subprocess.check_output(["git", "commit", "-a", "-m", "Remove JAVA_TOOL_OPTIONS (gets added by microservicecontroller)"], shell=False)

def alter_dump_copy_add_mongorestore():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "r", encoding="utf8") as otel_deployf:
            otel_deploy = otel_deployf.read()
        otel_deploy = otel_deploy.replace(" cp /persinit/persinit/ /app/", " cp -r /persinit/persinit/ /app/dumps/; cp /mongorestore/mongorestore_dir/mongorestore /app/")
        otel_deploy = otel_deploy.replace("persinit:latest", f"persinit:{branch}")

        otel_deploy = otel_deploy.replace("""          args: [ "-c", "cp -R /persinit /persinit-mnt/" ]""",
                                          """          args: [ "-c", "cp -R /persinit /persinit-mnt/" ]
        - name: mongorestore-container
          image: containers.github.scch.at/contest/trainticket/mongorestore:latest
          imagePullPolicy: Always
          volumeMounts:
            - name: mongorestore-vol
              mountPath: /mongorestore-mnt
          command: [ "/bin/sh" ]
          args: [ "-c", "cp -R /mongorestore_dir /mongorestore-mnt/" ]""")

        otel_deploy = otel_deploy.replace("""mountPath: /persinit
            - name: microservicecontroller-vol""",
                                          """mountPath: /persinit
            - name: mongorestore-vol
              mountPath: /mongorestore
            - name: microservicecontroller-vol""")
        otel_deploy = otel_deploy.replace("""        - name: microservicecontroller-vol
          emptyDir: {}""", """        - name: mongorestore-vol
          emptyDir: {}
        - name: microservicecontroller-vol
          emptyDir: {}""")

        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "w", encoding="utf8") as otel_deployf:
            otel_deployf.write(otel_deploy)
        subprocess.check_output(["git", "commit", "-a", "-m", "Alter copy command for dumps. Add mongorestore container"], shell=False)


def add_missing_startup_command_persist_init():
    otel_deployf = Path("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml")
    otel_deploy = otel_deployf.read_text(encoding="utf8")
    otel_deploy = otel_deploy.replace(" cp -R /persinit/persinit/ /app/", " cp -r /persinit/persinit/ /app/dumps/; cp /mongorestore/mongorestore_dir/mongorestore /app/")
    otel_deployf.write_text(otel_deploy, encoding="utf8")
    subprocess.check_output(["git", "commit", "-a", "-m", "Add missing copy command for mongorestore"], shell=False)


def tweak_resource_assignments():
    otel_deployf = Path("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml")
    otel_deploy = otel_deployf.read_text(encoding="utf8")
    otel_deploy = otel_deploy.replace("""\n              cpu: 500m""", "")
    otel_deploy = otel_deploy.replace("""            requests:
              cpu: 100m
              memory: 250Mi""","""            requests:
              cpu: 50m
              memory: 200Mi""")
    otel_deployf.write_text(otel_deploy, encoding="utf8")

    otel_coll_f = Path("./deployment/kubernetes-manifests/otel/otel.yaml")
    otel_coll = otel_coll_f.read_text(encoding="utf8")
    otel_coll = otel_coll.replace("""\n              cpu: 4000m""", "")
    otel_coll_f.write_text(otel_coll, encoding="utf8")
    subprocess.check_output(["git", "commit", "-a", "-m", "Tweak pod resource assignments"], shell=False)


def update_microservice_controller():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "r", encoding="utf8") as otel_deployf:
            otel_deploy = otel_deployf.read()
        otel_deploy = otel_deploy.replace("microservicecontroller:latest", "microservicecontroller:fault-branches")
        with open("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml", "w", encoding="utf8") as otel_deployf:
            otel_deployf.write(otel_deploy)
        subprocess.check_output(["git", "commit", "-a", "-m", "Use microservicecontroller of fault branches"], shell=False)


def update_spring_fox_and_evo_driver():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        # add_spring_fox_config()
        # subprocess.check_output(["git", "commit", "-a", "-m", "Generate swagger documentation only for classes with @RestController annotation"], shell=False)
        add_embedded_evo_master_controller()
        subprocess.check_output(["git", "commit", "-a", "-m", "Add missing imports"], shell=False)


def search_in_branches():
    regex = re.compile(r"^\s+proxy_pass\s+https?://ts-voucher-service", flags=re.MULTILINE)
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        path = Path("./ts-ui-dashboard/nginx.conf")
        if regex.search(path.read_text(encoding="utf8")):
            print(branch)


def adapt_dockerfiles():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        for f in glob("./../TrainTicket/ts-*/Dockerfile", recursive=True):
            p = Path(f)
            content = p.read_text(encoding="utf8")
            content = content.replace("RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone\n", "")
            p.write_text(content, encoding="utf8")
        try:
            subprocess.check_output(["git", "commit", "-a", "-m", "Remove timezone adaptation of service container"], shell=False)
        except Exception as e:
            print(f"Branch {branch}: Git commit error, maybe no changes where made: {e}")


def remove_zipkin_and_spring_sleuth():
    for f in glob("./../TrainTicket/ts-*/**/resources/application.yml", recursive=True):
        p = Path(f)
        content = p.read_text(encoding="utf8")
        content = content.replace("""  zipkin:
    baseUrl: http://zipkin:9411/
  sleuth:
    sampler:
      percentage: 1.0""", "")
        p.write_text(content, encoding="utf8")
    pom = Path("./../TrainTicket/pom.xml")
    pom_content = pom.read_text(encoding="utf8")
    pom_content = pom_content.replace("""		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-sleuth-core</artifactId>
			<version>1.3.0.RELEASE</version>
		</dependency>""", "")
    pom_content = pom_content.replace("""		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-sleuth-zipkin</artifactId>
			<version>1.3.0.RELEASE</version>
		</dependency>""", "")
    pom.write_text(pom_content, encoding="utf8")
    try:
        subprocess.check_output(["git", "commit", "-a", "-m", "Remove zipkin and spring sleuth tracing setup"], shell=False)
    except Exception as e:
        print(f"Git commit error, maybe no changes where made: {e}")

def adapt_otel_deploy():
    otel_deploy = Path("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml")
    otel_deploy_cont = otel_deploy.read_text(encoding="utf8")
    otel_deploy_cont = otel_deploy_cont.replace("""            limits:
          cpu: 500m
          memory: 2500Mi""",
                                                """            limits:
              cpu: 500m
              memory: 2500Mi""")
    otel_deploy.write_text(otel_deploy_cont, encoding="utf8")
    subprocess.check_output(["git", "commit", "-a", "-m", "Fix indentation"], shell=False)


def copy_files():
    for src, dst in file_mapping.items():
        shutil.copy(src, dst)
    subprocess.check_output(["git", "commit", "-a", "-m", "Increase prometheus memory limit"], shell=False)


def remove_scch_hpc_labels():
    to_clean = [
        "./deployment/kubernetes-manifests/otel/otel.yaml",
        "./deployment/kubernetes-manifests/quickstart-k8s/yamls/mongo-dbs.yml",
        "./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml",
        # "./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml.sample",  # Master
        # "./deployment/kubernetes-manifests/quickstart-k8s/yamls/deploy.yaml.sample",  # Master
        # "./deployment/kubernetes-manifests/quickstart-k8s/yamls/sw_deploy.yaml.sample",  # Master
    ]
    hpc_labels = re.compile(r"\n[# ]+hpc\.scch\.at/[a-zA-Z0-9_\-. :]+$", flags=re.MULTILINE)
    empty_labels = re.compile(r"^ *labels:\n( *spec:)", flags=re.MULTILINE)
    for path in to_clean:
        yaml = Path(path)
        text = yaml.read_text(encoding="utf8")
        text = hpc_labels.sub("", text)
        text = empty_labels.sub(r"\g<1>", text)
        yaml.write_text(text, encoding="utf8")
    subprocess.check_output(["git", "commit", "-a", "-m", "Remove internal deployment labels"], shell=False)


def replace_system_out_with_logger():
    contains_sout = re.compile(r"( +)System.out.println", flags=re.MULTILINE)
    class_name = re.compile(r"^ *(?:public|private)? +(?:static +)?(?:final +)?(?:final +)?(?:static +)?class +([a-zA-Z0-9_\-]+)", flags=re.MULTILINE)
    inside_class = re.compile(r"^ *(?:public|private)? +(?:static +)?(?:final +)?(?:final +)?(?:static +)?class +[a-zA-Z0-9_\- \n()@]+{", flags=re.MULTILINE)
    for j in glob("./**/*.java", recursive=True):
        java_file = Path(j)
        text = java_file.read_text(encoding="utf8")
        if contains_sout.search(text):
            text = contains_sout.sub(r"\g<1>logger.info", text)
            class_match = class_name.search(text)
            if not class_match:
                print(f"Could not find class name in {j}")
            class_n = class_match[1]
            in_class_match = inside_class.search(text)
            if not in_class_match:
                print(f"Could not locate inside class in {j}")
            if "    private final static org.slf4j.Logger logger" not in text \
                    and "Logger logger =" not in text:
                text = inside_class.sub(rf"\g<0>\n    private final static org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger({class_n}.class);", text, count=1)
            java_file.write_text(text, encoding="utf8")
    try:
        subprocess.check_output(["git", "commit", "-a", "-m", "Replace system out with logger"], shell=False)
    except Exception:
        print("No files updated")


def increase_log_file_size():
    for file in glob("./**/application.yml", recursive=True):
        path = Path(file)
        dst = path.parent
        shutil.copy("./../update_files_in_branches/files_to_update/logback-spring.xml", dst)
        subprocess.check_output(["git", "add", f"{dst}/logback-spring.xml"], shell=False)
    subprocess.check_output(["git", "commit", "-a", "-m", "Add default logback configuration with adapted file size limit"], shell=False)


def adapt_jvm_time_zone():
    otel_deployf = Path("./deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml")
    otel_deploy = otel_deployf.read_text(encoding="utf8")
    otel_deploy = otel_deploy.replace("cd /app/;", "cd /app/;export TZ='Europe/Rome';")
    otel_deployf.write_text(otel_deploy, encoding="utf8")
    subprocess.check_output(["git", "commit", "-a", "-m", "Adapt JVM timezone to Europe/Rome"], shell=False)
    # "export TZ='Europe/Rome';


def remove_empty_logging_calls():
    replaced = False
    for j in glob("./**/*.java", recursive=True):
        java_file = Path(j)
        text = java_file.read_text(encoding="utf8")
        if "logger.info();" in text:
            text = text.replace("logger.info();", "")
            java_file.write_text(text, encoding="utf8")
            replaced = True
    if replaced:
        subprocess.check_output(["git", "commit", "-a", "-m", "Remove empty logging calls"], shell=False)


def add_mongo_db_empty_collections_where_not_present(branch:str):
    mongos = {
        "ts-account-mongo/ts/": "login_user_list",
        "ts-assurance-mongo/ts/": "assurance",
        "ts-food-mongo/ts/": "foodorder",
        "ts-order-mongo/test/": "ordersSUFFIX", # same contents as order-other except for uuid value. Probably negligible but just be sure
        "ts-order-other-mongo/test/": "orders",
        "ts-consign-mongo/ts/": "consign_record",
    }
    os.makedirs("../update_files_in_branches/tmp/", exist_ok=True)
    shutil.unpack_archive(f"../update_files_in_branches/dump_archives_original/dumps-{branch}.tar.gz", extract_dir="../update_files_in_branches/tmp", format="gztar")
    new_file = False
    for path, collection in mongos.items():
        coll = collection.replace("SUFFIX", "")
        if (pathlib.Path(f"../update_files_in_branches/tmp/{path}").exists() and
                True in [f.startswith(coll) for f in os.listdir(f"../update_files_in_branches/tmp/{path}")]):
            print(f"{coll} already present in {path} in branch {branch}")
        else:
            print(f"Adding {coll} to {path} in branch {branch}")
            os.makedirs(f"../update_files_in_branches/tmp/{path}/", exist_ok=True)
            shutil.copy(f"../update_files_in_branches/files_to_update/dumps/{coll}.bson", f"../update_files_in_branches/tmp/{path}/{coll}.bson")
            shutil.copy(f"../update_files_in_branches/files_to_update/dumps/{collection}.metadata.json", f"../update_files_in_branches/tmp/{path}/{coll}.metadata.json")
            new_file = True
    if new_file:
        shutil.make_archive(base_name=f"./PersistenceInit/dumps", format="gztar", root_dir="../update_files_in_branches/tmp/", )
        subprocess.check_output(["git", "commit", "-a", "-m", "Add mongoDB schemas not present at system startup (fix wrong file names)"], shell=False)
    shutil.rmtree("../update_files_in_branches/tmp/")


def create_enhanced_mongo_db_dumps_for_all_branches(branch:str):
    mongos = {
        "ts-account-mongo/ts/": "login_user_list",
        "ts-assurance-mongo/ts/": "assurance",
        "ts-food-mongo/ts/": "foodorder",
        "ts-order-mongo/test/": "ordersSUFFIX", # same contents as order-other except for uuid value. Probably negligible but just be sure
        "ts-order-other-mongo/test/": "orders",
        "ts-consign-mongo/ts/": "consign_record",
    }
    os.makedirs("../update_files_in_branches/tmp/", exist_ok=True)
    shutil.unpack_archive(f"../update_files_in_branches/dump_archives_original/dumps-{branch}.tar.gz", extract_dir="../update_files_in_branches/tmp", format="gztar")
    for path, collection in mongos.items():
        coll = collection.replace("SUFFIX", "")
        if (pathlib.Path(f"../update_files_in_branches/tmp/{path}").exists() and
                True in [f.startswith(coll) for f in os.listdir(f"../update_files_in_branches/tmp/{path}")]):
            print(f"{coll} already present in {path} in branch {branch}")
        else:
            print(f"Adding {coll} to {path} in branch {branch}")
            os.makedirs(f"../update_files_in_branches/tmp/{path}/", exist_ok=True)
            shutil.copy(f"../update_files_in_branches/files_to_update/dumps/{coll}.bson", f"../update_files_in_branches/tmp/{path}/{coll}.bson")
            shutil.copy(f"../update_files_in_branches/files_to_update/dumps/{collection}.metadata.json", f"../update_files_in_branches/tmp/{path}/{coll}.metadata.json")

    shutil.make_archive(base_name=f"../update_files_in_branches/dump_archives_enhanced/dumps-enhanced-{branch}", format="gztar", root_dir="../update_files_in_branches/tmp/", )
    shutil.rmtree("../update_files_in_branches/tmp/")


def copy_files_to_wsl():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        shutil.copytree("../TrainTicket", "\\\\wsl.localhost\\Ubuntu-20.04\home\\urb\\traintickets\\" + branch, dirs_exist_ok=True)
    # Execute the following commands from the base folder
    # Handle character encoding issues
    # Add execute permissions
    for i in range(1, 23):
        print(f'''chmod +x ./ts-error-F{i}/script/publish-docker-images.sh;chmod +x ./ts-error-F{i}/hack/deploy/specific-reset.sh;chmod +x ./ts-error-F{i}/hack/deploy/deploy.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/hack/deploy/specific-reset.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/hack/deploy/deploy.sh;chmod +x ./ts-error-F{i}/PersistenceInit/publish-persinit-image.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/PersistenceInit/publish-persinit-image.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/script/publish-docker-images.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/hack/deploy/utils.sh''')
    print("\n\n")
    # Build maven. Hint: execute in multiple terminals for speedup
    for i in range(1, 23):
        print(f"cd ts-error-F{i};mvn -DskipTests=true clean package;cd ..; ")
    print("\n\n")
    # Build and push docker images. Hint: execute in multiple terminals for speedup
    for i in range(1, 23):
        print(f'''cd ./ts-error-F{i}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')
    for i in range(1, 23):
        print(f'''cd ./ts-error-F{i}; ./PersistenceInit/publish-persinit-image.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')


def chmod_for_scripts():
    for f in glob("./**/*.sh",recursive=True):
        subprocess.check_output(["git", "update-index", "--chmod=+x", f], shell=False)
    subprocess.check_output(["git", "commit", "-a", "-m", "Add execute permission in git"], shell=False)


def distribute_mongo_dumps():
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        shutil.copy(f"../update_files_in_branches/dumps-{branch}.tar.gz", "./PersistenceInit/dumps.tar.gz")
        subprocess.check_output(["git", "commit", "-a", "-m", "Add final mongo dumps for restoring dumps"], shell=False)

def add_testing_dependencies_to_pom():
    pom = Path("./../TrainTicket/pom.xml")
    pom_content = pom.read_text(encoding="utf8")
    pom_content = pom_content.replace("""	</dependencies>""",
                                      """		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
			<version>1.5.22.RELEASE</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/io.rest-assured/rest-assured -->
		<dependency>
			<groupId>io.rest-assured</groupId>
			<artifactId>rest-assured</artifactId>
			<version>3.3.0</version>
			<scope>test</scope>
		</dependency>

	</dependencies>""")
    pom.write_text(pom_content, encoding="utf8")
    try:
        subprocess.check_output(["git", "commit", "-a", "-m", "Add test dependencies for executing generated EvoMaster tests"], shell=False)
    except Exception:
        print("No files updated")

def undo_last_commits():
    # for branch in branches:
        # subprocess.check_output(["git", "checkout", branch], shell=False)
        # subprocess.check_output(["git", "reset", "HEAD~"], shell=False)
        # subprocess.check_output(["git", "restore", "deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml"], shell=False)
        # subprocess.check_output(["git", "reset", "HEAD~"], shell=False)
        # for f in glob("./ts-*/**/EmbeddedEvoMasterController.java", recursive=True):
        #     p = Path(f)
        #     subprocess.check_output(["git", "restore", p.as_posix()], shell=False)
        #
    subprocess.check_output(["git", "reset", "HEAD~"], shell=False)
    subprocess.check_output(["git", "restore", "PersistenceInit/dumps.tar.gz"], shell=False)
    # subprocess.check_output(["git", "reset", "HEAD~"], shell=False)
    # for f in glob("./**/*HttpAspect*.java", recursive=True):
    #     p = Path(f)
    #     subprocess.check_output(["git", "restore", p.as_posix()], shell=False)
    # try:
    #     subprocess.check_output(["git", "commit", "-a", "-m", "Replace system out with logger in unintendedly missed files"], shell=False)
    # except Exception:
    #     print("No files updated")

if __name__ == '__main__':
    os.chdir("./../TrainTicket")
    # update_branches()
    # search_in_branches()
    # copy_files_to_wsl()
    # adapt_dockerfiles()
    # remove_java_tool_options()
    # alter_dump_copy_add_mongorestore()
    # undo_last_commits()
    # update_spring_fox_and_evo_driver()

    for branch in branches:
        # subprocess.check_output(["git", "checkout", branch], shell=False)
        # undo_last_commits()
        # add_testing_dependencies_to_pom()
        # chmod_for_scripts()
        # remove_empty_logging_calls()
        # increase_log_file_size()
        # adapt_jvm_time_zone()
        # subprocess.check_output(["git", "commit", "--amend", "-m", "Replace system out with logger in unintendedly missed files"], shell=False)
        # undo_last_commits()
        # replace_system_out_with_logger()
        # remove_scch_hpc_labels()
        # tweak_resource_assignments()
        # add_embedded_evo_master_controller(ssl=branch == "ts-error-F4")
        # add_mongo_db_empty_collections_where_not_present(branch)
        create_enhanced_mongo_db_dumps_for_all_branches(branch)
        # adapt_otel_deploy()
        # remove_zipkin_and_spring_sleuth()

    # undo_last_commits()
    # subprocess.check_output(["git", "checkout", "ts-error-F1"], shell=False)
    # Execute: git push --all


