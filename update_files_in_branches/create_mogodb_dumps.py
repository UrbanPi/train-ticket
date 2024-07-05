import http
import logging
import os
import shutil
import ssl
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib import request

from service_availability import filter_services

plain_format = logging.Formatter("%(message)s")
regular_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger_handler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger()  # Logger
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)
logger_handler.setFormatter(regular_format)

branches = [
    # "master",
    "ts-error-F1",
    "ts-error-F2",
    "ts-error-F3",
    "ts-error-F4",
    "ts-error-F5",
    "ts-error-F6",
    "ts-error-F7", "ts-error-F8",
    "ts-error-F9", "ts-error-F10",
    "ts-error-F11", "ts-error-F12",
    "ts-error-F13", "ts-error-F14", "ts-error-F15", "ts-error-F16", "ts-error-F17", "ts-error-F18",
    "ts-error-F19", "ts-error-F20", "ts-error-F21", "ts-error-F22"

]


def check_service_availability(services_to_check: list[dict], https:bool = False):
    with ThreadPoolExecutor() as executor:
        wait_count = 0
        while len(services_to_check) != 0:
            results = executor.map(check_readiness, services_to_check, [https]*len(services_to_check))
            services_to_check = []
            for res in results:
                if res:
                    services_to_check.append(res[0])
                    # if res[1]:
                    #     logger.error(f"{res[0].get('name')}\n{res[1]}")
            if len(services_to_check) != 0:
                # logger_handler.terminator = "\x1b[1K\r"  # Clear line, carriage return
                logger_handler.terminator = ""
                logger.info(
                    f"\x1b[1K\rWaiting on {len(services_to_check)} services to get ready: {','.join([s.get('name') for s in services_to_check])}")
                logger_handler.terminator = "\n"
                time.sleep(10)
                if wait_count > 36:
                    logger.info(
                        f"Waited for around 6 minutes on services {','.join([s.get('name') for s in services_to_check])}. Restarting them now.")
                    logger.info("Stopping services and waiting for 30 sec...")
                    call_microservice_controller_of(services_to_check, stop_service)
                    time.sleep(30)
                    logger.info("Starting services and waiting for 3 min")
                    call_microservice_controller_of(services_to_check, start_service)
                    time.sleep(60 * 3)
                    wait_count = 0
            wait_count += 1

    executor.shutdown(wait=True)


def check_readiness(service: dict, https: bool=False):
    try:
        if https:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            url = f"https://localhost:{service.get('port') - 600}/v2/api-docs"
            res: http.client.HTTPResponse = request.urlopen(url, context=ctx, timeout=30)
        else:
            url = f"http://localhost:{service.get('port') - 600}/v2/api-docs"
            res: http.client.HTTPResponse = request.urlopen(url, timeout=30)
        if res.status != 200:
            return service, None
    except Exception as e:
        return service, e

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    #     s.connect((url, service.get('port') - 600))
    # except ConnectionRefusedError as e:
    #     return service, e


def call_microservice_controller_of(services: list[dict], with_method):
    with ThreadPoolExecutor() as executor:
        results = executor.map(with_method, services)
        for res in filter(None, results):
            if res.startswith("Error"):
                logger.error("{}".format(res))
            else:
                logger.info("{}".format(res))
    executor.shutdown(wait=True)


def start_service(service: dict):
    url = f"http://localhost:{service.get('port')}/api/control/startNormal"
    try:
        response: str = request.urlopen(url, timeout=30).read().decode("utf8")
        if not response.startswith("Starting main Spring application"):
            return f"Could not start service {service.get('name')}: {response}"
    except Exception as e:
        return f"Error when starting service {service.get('name')}:\n{e}"


def stop_service(service: dict):
    url = f"http://localhost:{service.get('port')}/api/control/stop"
    try:
        response: str = request.urlopen(url, timeout=30).read().decode("utf8")
        if not response.startswith("Stopping jar"):
            return f"Could not stop service {service.get('name')}:\n{response}"
    except Exception as e:
        return f"Error when stopping service {service.get('name')}:\n{e}"

def copy_from_kubernetes_pod_to(pod_name: str, pod_src: str, destination: str, service_name: str, thing_to_copy: str):
    service_and_file = pod_name + pod_src
    sub = subprocess.run(["kubectl", "-c", service_name, "cp", service_and_file, destination])
    if sub.returncode != 0:
        return f"No {thing_to_copy} for {pod_name}"


def dump_mongos(service_name:str, pod_name:str):
    sub = subprocess.run(["kubectl", "exec", "-c", service_name, pod_name, "--", "mongodump"])
    if sub.returncode != 0:
        return f"Could not create dump for mongoDB on {pod_name}"



def create_dumps(branch:str):
    selected_services, service_to_test = filter_services(branch)
    all_services: list[dict] = selected_services

    #  Start all services to create initial data
    call_microservice_controller_of(services=all_services, with_method=start_service)

    check_service_availability(all_services, https=branch == "ts-error-F4")

    #  Connect to each monogdb instance and dump the database kubectl get pods
    mongodb_pods = list(filter(lambda x: "-mongo-" in x, subprocess.check_output(["kubectl", "get", "pods", "-o", "name"],
                                                                                 shell=False).decode("utf8").replace("pod/","").split("\n")))
    mongodb_services = [mon[0:mon.rfind("-mongo-")]+"-mongo" for mon in mongodb_pods]

    logger.info("Dumping mongoDBs in pods...")
    with ThreadPoolExecutor() as executor:
        results = executor.map(dump_mongos, mongodb_services, mongodb_pods)
        for res in results:
            if res:
                logger.error(res)
    executor.shutdown(wait=True)

    base_destination = "./dumps/"
    # Clean up previous data
    if os.path.exists(base_destination):
        shutil.rmtree(base_destination)

    # Re-create directories
    os.makedirs(base_destination, exist_ok=True)

    #  Download dump and rename to originating mongodb instance
    pod_nb = len(mongodb_pods)
    logger.info("Downloading dumps...")
    with ThreadPoolExecutor() as executor:
        results = executor.map(copy_from_kubernetes_pod_to, mongodb_pods,
                               [":dump"] * pod_nb,
                               [f"./{base_destination}/{s}" for s in mongodb_services],
                               mongodb_services,
                               ["mongoDB dumps"] * pod_nb)
        for res in results:
            if res:
                logger.error(res)
    executor.shutdown(wait=True)
    logger.info("Creating archive")
    #  tar.gz the final files
    shutil.make_archive(f"./dumps-{branch}", "gztar", root_dir=base_destination)
    logger.info("Finished!")



#  Add mongorestore (chmod +x)
#  In EvoDriver restore every dump with mongorestore

def extract_deploy_yamls():
    for branch in branches:
        os.chdir("./../TrainTicket/")
        subprocess.check_output(["git", "checkout", branch], shell=False)
        os.chdir("./../update_files_in_branches/")
        shutil.copytree("./../TrainTicket/deployment/kubernetes-manifests/quickstart-k8s/yamls/", "./deployments/" + branch, dirs_exist_ok=True)


def distribute_mongo_dumps():
    os.chdir("./../TrainTicket/")
    for branch in branches:
        subprocess.check_output(["git", "checkout", branch], shell=False)
        shutil.copy(f"./../update_files_in_branches/dumps-{branch}.tar.gz", "./PersistenceInit/dumps.tar.gz")
        shutil.copy(f"./../update_files_in_branches/dumps-{branch}.tar.gz",  f"\\\\wsl.localhost\\Ubuntu-20.04\home\\urb\\traintickets\\{branch}\\PersistenceInit\\dumps.tar.gz")


        try:
            subprocess.check_output(["git", "commit", "-a", "-m", "Add final mongo dumps for restoring (assure correct dump is copied)"], shell=False)
        except Exception as e:
            print(e)

    for i in range(1, 23):
        print(f"chmod +x ./ts-error-F{i}/PersistenceInit/publish-persinit-image.sh;sed -i -e 's/\\r$//' ./ts-error-F{i}/PersistenceInit/publish-persinit-image.sh")
    print("\n\n")

    for i in range(1, 23):
        print(f'''cd ./ts-error-F{i}; ./PersistenceInit/publish-persinit-image.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')


if __name__ == '__main__':
    # subprocess.check_output(["helm", "install", "rabbitmq", "./charts/rabbitmq", "-n", "default", ], shell=False)
    # for branch in branches[16:22]:
    #     logger.info(f"Setup branch {branch}")
    #     subprocess.check_output(["kubectl", "apply", "-f", "./deployments/"+branch+ "/"], shell=False)
    #     logger.info("Sleeping 5min")
    #     time.sleep(60*5)
    #     logger.info("Creating dumps")
    #     create_dumps(branch)
    #     subprocess.check_output(["kubectl", "delete", "-f", "./deployments/"+branch+ "/"], shell=False)
    #     logger.info("Sleeping 20sec")
    #     time.sleep(20)
    # subprocess.check_output(["heml", "uninstall", "rabbitmq", "-n", "default"], shell=False)
    distribute_mongo_dumps()
    # subprocess.check_output(["git", "checkout", "ts-error-F1"], shell=False)

    # create_dumps("ts-error-F4")
    # extract_deploy_yamls()
    # 1. deploy on remote desktops (new version)
    # 2. Check service availability
    # 3. Follow above script
